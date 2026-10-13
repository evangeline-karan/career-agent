import streamlit as st
from agent import analyze, explain

st.set_page_config(page_title="Explainable Career AI Agent", page_icon="🧭")

st.title("🧭 Explainable Career AI Agent")
st.write("Type your skills and see which roles fit you, and exactly why.")

skills_text = st.text_input(
    "Your skills (separate with commas)",
    placeholder="python, sql, excel",
)

if st.button("Analyze my skills"):
    skills = skills_text.split(",")

    if not any(s.strip() for s in skills):
        st.warning("Please type at least one skill.")
    else:
        results = analyze(skills)

        st.subheader("Role matches")
        for r in results:
            st.markdown(f"**{r['role']}**: {r['score']}/100")
            st.progress(r["score"] / 100)

            col1, col2 = st.columns(2)
            with col1:
                st.success("✅ Matched")
                if r["matched"]:
                    for skill, marks in r["matched"].items():
                        st.write(f"{skill} (+{marks})")
                else:
                    st.write("None yet")
            with col2:
                st.error("❌ Missing")
                for skill, marks in r["missing"].items():
                    st.write(f"{skill} (-{marks})")

        st.subheader("AI explanation for your top role")
        with st.spinner("Thinking..."):
            st.info(explain(results[0]))