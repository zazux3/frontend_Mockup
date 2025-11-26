import streamlit as st
from pipeline import run_pipeline   # mock version of run_pipeline 

st.set_page_config(page_title="COMP248 — Banking & Finance Assistant (Team 3)", layout="wide")
st.title("COMP248 — Banking & Finance Assistant (Team 3)")

st.markdown(
    """
    **Demonstration:** Single worker agent using RAG (ChromaDB if available) + Reflection Agent.
    - Enter a finance question and press **Ask**.
    - If ChromaDB is not prepared, the app will use a placeholder retrieval so the demo still works.
    """
)

# sidebar for status / actions
with st.sidebar:
    st.header("Prototype Controls")
    use_chroma = st.checkbox("Attempt to use ChromaDB (if installed)", value=True)
    st.markdown("**Data ingestion**")
    uploaded_pdf = st.file_uploader("(Optional) Upload a PDF to ingest to ChromaDB", type=["pdf"])
    if uploaded_pdf is not None:
        st.info("Uploaded PDF will be processed locally for demo only (not persisted).")

    st.markdown("---")
    st.markdown("**Team info**")
    st.write("Group 3 — Wednesday demo")
    st.write("Prepared by: Team 3 (COMP248)")

question = st.text_area("Enter your finance question:", height=130, placeholder="e.g. How do rising interest rates affect mortgage costs in Canada?")

col1, col2 = st.columns([1,1])
with col1:
    if st.button("Ask"):
        if not question.strip():
            st.warning("Please enter a question first.")
        else:
            with st.spinner("Running Planner → Research (RAG) → Reflection..."):
                # ensure_chromadb_ready will ingest uploaded_pdf into a temp chroma if provided and libs available
                result = run_pipeline(question, use_chroma=use_chroma, uploaded_pdf=uploaded_pdf)
            # Display results
            st.subheader("Draft Answer (from worker agent)")
            st.write(result.get("draft_answer", "—"))
            st.subheader("Final Answer (after Reflection agent)")
            st.success(result.get("final_answer", "—"))

            st.subheader("Retrieved Chunks / Evidence")
            retrieved = result.get("retrieved_chunks", [])
            if not retrieved:
                st.write("No chunks returned.")
            else:
                for i, c in enumerate(retrieved, 1):
                    st.write(f"**Chunk {i} — {c.get('source','unknown')} (p.{c.get('page', '?')})**")
                    st.write(c.get("text", "")[:1000] + ("..." if len(c.get("text",""))>1000 else ""))
                    st.write("---")

with col2:
    st.subheader("Debug / Metadata")
    st.json({
        "planner_route": result.get("planner_route") if 'result' in locals() else None,
        "chroma_used": result.get("chroma_used") if 'result' in locals() else None,
        "model_used_for_reflection": result.get("reflection_model", None) if 'result' in locals() else None
    })

st.caption("⚖️ Demo is educational. Not financial advice.")