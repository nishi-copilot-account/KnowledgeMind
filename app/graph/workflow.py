"""
KnowledgeMind Workflow.
"""

from langgraph.graph import StateGraph, START, END

from app.graph.state import KnowledgeState
from app.retrieval.retriever import KnowledgeRetriever
from app.reasoning.reasoning_agent import ReasoningAgent
from app.llm.llm_service import LLMService

from app.agents.planner_agent import PlannerAgent
from app.agents.chat_agent import ChatAgent
from app.agents.summary_agent import SummaryAgent
from app.agents.compare_agent import CompareAgent
from app.agents.question_rewriter import QuestionRewriter
from app.agents.analysis_agent import AnalysisAgent

from app.utils.logger import logger


class KnowledgeWorkflow:

    def __init__(self):

        self.planner = PlannerAgent()

        self.retriever = KnowledgeRetriever()

        self.reasoner = ReasoningAgent()

        self.analysis_agent = AnalysisAgent()

        self.llm = LLMService()

        self.chat_agent = ChatAgent()

        self.summary_agent = SummaryAgent()

        self.compare_agent = CompareAgent()

        self.rewriter = QuestionRewriter()

        self.graph = StateGraph(KnowledgeState)

        # -------------------------------------------------
        # Nodes
        # -------------------------------------------------

        self.graph.add_node("plan", self.plan_node)
        self.graph.add_node("chat", self.chat_node)
        self.graph.add_node("summarize", self.summarize_node)
        self.graph.add_node("compare", self.compare_node)
        self.graph.add_node("rewrite", self.rewrite_node)
        self.graph.add_node("retrieve", self.retrieve_node)
        self.graph.add_node("reason", self.reason_node)
        self.graph.add_node("analyze", self.analyze_node)
        self.graph.add_node("generate", self.generate_node)

        # -------------------------------------------------
        # Edges
        # -------------------------------------------------

        self.graph.add_edge(START, "plan")

        self.graph.add_conditional_edges(
            "plan",
            self.route,
            {
                "retrieve": "rewrite",
                "chat": "chat",
                "summarize": "summarize",
                "compare": "compare",
            },
        )

        self.graph.add_edge("chat", END)
        self.graph.add_edge("summarize", END)
        self.graph.add_edge("compare", END)

        self.graph.add_edge("rewrite", "retrieve")
        self.graph.add_edge("retrieve", "reason")
        self.graph.add_edge("reason", "analyze")
        self.graph.add_edge("analyze", "generate")
        self.graph.add_edge("generate", END)

    ###########################################################
    # Helpers
    ###########################################################

    def _add_workflow_step(
        self,
        state: KnowledgeState,
        step: str,
    ) -> None:

        state.setdefault(
            "workflow_steps",
            [],
        ).append(step)

    def _add_explanation(
        self,
        state: KnowledgeState,
        explanation: str,
    ) -> None:

        state.setdefault(
            "explanation",
            [],
        ).append(explanation)

    ###########################################################
    # Planner
    ###########################################################

    def plan_node(
        self,
        state: KnowledgeState,
    ) -> KnowledgeState:

        has_history = bool(
            state.get("history")
        )

        action = self.planner.plan(
            question=state["question"],
            has_history=has_history,
        )

        logger.info(
            "Planner selected action: %s",
            action,
        )

        state["action"] = action

        self._add_explanation(
            state,
            f"Planner selected '{action}' workflow based on the user's question.",
        )

        self._add_workflow_step(
            state,
            "🧠 Planner\n"
            f"   ✓ Selected '{action}' workflow",
        )

        return state


    def route(
        self,
        state: KnowledgeState,
    ) -> str:

        return state["action"]

    ###########################################################
    # Chat
    ###########################################################

    def chat_node(
        self,
        state: KnowledgeState,
    ) -> KnowledgeState:

        state["answer"] = self.chat_agent.respond(
            state["question"],
        )

        self._add_workflow_step(
            state,
            "💬 Chat Agent",
        )

        self._add_explanation(
            state,
            "Handled the request as a general conversation without retrieving documents.",
        )

        return state

    ###########################################################
    # Summary
    ###########################################################

    def summarize_node(
        self,
        state: KnowledgeState,
    ) -> KnowledgeState:

        results = self.retriever.retrieve(
            question=state["question"],
            top_k=5,
            source_document=state.get(
                "selected_document",
                "",
            ),
        )

        context = self.reasoner.prepare_context(
            results,
            state["question"],
            history=state.get(
                "history",
                "",
            ),
        )
        state["search_results"] = results
        state["answer"] = self.summary_agent.summarize(
            context,
        )

        self._add_workflow_step(
            state,
            f"🔍 Retriever\n"
            f"   ✓ Search Scope: {state.get('selected_document') or 'All Documents'}\n"
            f"   ✓ Retrieved {len(results)} chunks",
        )

        self._add_workflow_step(
            state,
            "🧩 Context Builder\n"
            "   ✓ Prepared document context\n"
            "   ✓ Removed duplicate chunks",
        )

        self._add_workflow_step(
            state,
            "📝 Summary Agent\n"
            "   ✓ Generated concise summary",
        )

        self._add_explanation(
            state,
            "Planner recognized a summarization request.",
        )

        self._add_explanation(
            state,
            f"Search scope: {state.get('selected_document') or 'All Documents'}.",
        )

        self._add_explanation(
            state,
            f"Retrieved {len(results)} relevant chunks.",
        )

        self._add_explanation(
            state,
            "Built a unified document context.",
        )

        self._add_explanation(
            state,
            "Generated the final summary using the retrieved content.",
        )



        return state

    ###########################################################
    # Compare
    ###########################################################

    def compare_node(
        self,
        state: KnowledgeState,
    ) -> KnowledgeState:

        results = self.retriever.retrieve(
            question=state["question"],
            top_k=5,
            source_document=state.get(
                "selected_document",
                "",
            ),
        )
       
        state["search_results"] = results

        self._add_workflow_step(
            state,
            f"🔍 Retriever\n"
            f"   ✓ Search Scope: {state.get('selected_document') or 'All Documents'}\n"
            f"   ✓ Retrieved {len(results)} relevant chunks",
        )

        context = self.reasoner.prepare_context(
            results,
            state["question"],
            history=state.get(
                "history",
                "",
            ),
            action="compare",
        )

        self._add_workflow_step(
        state,
        "🧩 Context Builder\n"
        "   ✓ Prepared document context\n"
        "   ✓ Removed duplicate chunks\n"
        "   ✓ Added conversation history"
            )

        state["answer"] = self.compare_agent.compare(
            context,
        )

        self._add_workflow_step(
            state,
            "⚖️ Compare Agent\n"
            "   ✓ Compared retrieved documents"
        )

        self._add_explanation(
            state,
            f"Retrieved {len(results)} relevant chunks to compare information across documents.",
        )

        self._add_explanation(
            state,
            "Planner recognized that the user requested a document comparison.",
        )

        self._add_explanation(
            state,
            "Prepared a comparison context from the retrieved documents.",
        )

        self._add_explanation(
            state,
            "The Compare Agent identified similarities and differences between the retrieved documents.",
        )

        self._add_explanation(
            state,
            f"Search was restricted to: {state.get('selected_document') or 'All Documents'}.",
        )

        self._add_explanation(
            state,
            f"{len(results)} relevant chunks were retrieved from the vector database.",
        )

        self._add_explanation(
            state,
            "The retrieved chunks were combined into a comparison context.",
        )

        self._add_explanation(
            state,
            "The Compare Agent generated the final comparison using the retrieved documents.",
        )

        return state

    ###########################################################
    # Rewrite
    ###########################################################

    def rewrite_node(
        self,
        state: KnowledgeState,
    ) -> KnowledgeState:

        history = state.get(
            "history",
            "",
        )

        rewritten = self.rewriter.rewrite(
            question=state["question"],
            history=history,
        )

        logger.info(
            "Rewritten question: %s",
            rewritten,
        )

        state["question"] = rewritten

        self._add_workflow_step(
            state,
            "✍️ Question Rewriter",
        )

        if rewritten != state["original_question"]:

            self._add_explanation(
                state,
                "The follow-up question was rewritten into a standalone question using conversation history.",
            )

        else:

            self._add_explanation(
                state,
                "The original question was already clear and required no rewriting.",
            )

        return state

    ###########################################################
    # Retrieve
    ###########################################################

    def retrieve_node(
        self,
        state: KnowledgeState,
    ) -> KnowledgeState:

        logger.info(
            "Executing Retrieve Node"
        )
        logger.info(
            "Search Scope: %s",
            state.get("selected_document") or "All Documents",
        )
        results = self.retriever.retrieve(
            question=state["question"],
            top_k=5,
            source_document=state.get(
                "selected_document",
                "",
    ),
        )

        state["search_results"] = results

        self._add_workflow_step(
            state,
            f"🔍 Retriever\n"
            f"   ✓ Search Scope: {state.get('selected_document') or 'All Documents'}\n"
            f"   ✓ Retrieved {len(results)} relevant chunks",
        )

        self._add_explanation(
            state,
            f"Retrieved {len(results)} relevant knowledge chunks from the vector database.",
        )

        return state

    ###########################################################
    # Reason
    ###########################################################

    def reason_node(
        self,
        state: KnowledgeState,
    ) -> KnowledgeState:

        logger.info(
            "Executing Reason Node"
        )

        context = self.reasoner.prepare_context(
            state["search_results"],
            question=state["question"],
            history=state.get(
                "history",
                "",
            ),
            action=state["action"],
        )

        state["context"] = context

        self._add_workflow_step(
            state,
            "🧠 Reasoning Agent\n"
            "   ✓ Combined retrieved knowledge\n"
            "   ✓ Included conversation history",
     )

        self._add_explanation(
            state,
            "Prepared structured context by combining retrieved knowledge and conversation history.",
        )
        return state

    ###########################################################
    # Analyze
    ###########################################################

    def analyze_node(
        self,
        state: KnowledgeState,
    ) -> KnowledgeState:

        logger.info(
            "Executing Analysis Node"
        )

        state["context"] = self.analysis_agent.analyze(
            context=state["context"],
            question=state["question"],
        )

        self._add_workflow_step(
            state,
            "📊 Analysis Agent",
        )

        self._add_explanation(
            state,
            "Applied deterministic analysis where applicable before generating the answer.",
        )

        return state

    ###########################################################
    # Generate
    ###########################################################

    def generate_node(
        self,
        state: KnowledgeState,
    ) -> KnowledgeState:

        logger.info(
            "Executing Generate Node"
        )

        state["answer"] = self.llm.generate(
            question=state["question"],
            context=state["context"],
        )

        self._add_workflow_step(
            state,
            "🤖 Response Generator\n"
            "   ✓ Generated final answer",
        )

        self._add_explanation(
            state,
            "Generated the final natural language response using the prepared context.",
        )

        return state

    ###########################################################

    ###########################################################
    # Helpers
    ###########################################################

    
    def compile(self):

        return self.graph.compile()