from typing import Optional


class DiagramGenerator:
    @staticmethod
    def save_mermaid_diagram(output_file: str = "agent_diagram.md") -> str:
        mermaid_code = """
graph TD
    A[JD Summarizer Agent] -->|Passes JD summaries| C[Matching Agent]
    B[CV Extractor Agent] -->|Passes parsed CVs| C
    C -->|Passes match scores| D[Shortlisting Agent]
    D -->|Passes shortlisted candidates| E[Interview Scheduler Agent]
""".strip()

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(f"# Agent Interaction Diagram\n\n```mermaid\n{mermaid_code}\n```\n")

        return output_file

    @staticmethod
    def generate_matplotlib_diagram(output_file: str = "agent_diagram.png") -> str:
        try:
            import matplotlib.pyplot as plt
            import networkx as nx

            graph = nx.DiGraph()
            graph.add_edges_from(
                [
                    ("JD Summarizer", "Matcher"),
                    ("CV Extractor", "Matcher"),
                    ("Matcher", "Shortlister"),
                    ("Shortlister", "Interview Scheduler"),
                ]
            )

            plt.figure(figsize=(10, 6))
            pos = nx.spring_layout(graph, seed=42)
            nx.draw_networkx(
                graph,
                pos,
                with_labels=True,
                node_size=2800,
                node_color="#8ecae6",
                arrows=True,
                font_size=10,
            )
            plt.axis("off")
            plt.tight_layout()
            plt.savefig(output_file, dpi=200)
            plt.close()
            return output_file
        except Exception:
            return DiagramGenerator.save_mermaid_diagram("agent_diagram.md")
