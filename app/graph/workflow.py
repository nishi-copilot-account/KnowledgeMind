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
    # Helper
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

        self._add_workflow_step(
            state,
            "🧠 Planner",
        )

        return state

    ###########################################################

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

        return state

    ###########################################################
    # Summary
    ###########################################################

    def summarize_node(
        self,
        state: KnowledgeState,
    ) -> KnowledgeState:

        results = self.retriever.retrieve(
            state["question"],
            top_k=5,
        )

        context = self.reasoner.prepare_context(
            results,
            state["question"],
            history=state.get(
                "history",
                "",
            ),
        )

        state["answer"] = self.summary_agent.summarize(
            context,
        )

        self._add_workflow_step(
            state,
            "📝 Summary Agent",
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
            state["question"],
            top_k=10,
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

        state["answer"] = self.compare_agent.compare(
            context,
        )

        self._add_workflow_step(
            state,
            "⚖️ Compare Agent",
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

        results = self.retriever.retrieve(
            state["question"],
            top_k=3,
        )

        state["search_results"] = results

        self._add_workflow_step(
            state,
            "🔍 Retriever",
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
            "🧠 Reasoning Agent",
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
            "🤖 LLM",
        )

        return state

    ###########################################################

    def compile(self):

        return self.graph.compile()