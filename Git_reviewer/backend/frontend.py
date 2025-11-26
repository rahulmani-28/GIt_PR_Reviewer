import streamlit as st
import requests

st.set_page_config(page_title="AI Code Reviewer", layout="wide")

st.title("🤖 AI Pull Request Reviewer")
st.markdown("Enter a GitHub Pull Request URL to get an instant AI review.")


repo_url = st.text_input("GitHub PR URL", placeholder="https://github.com/owner/repo/pull/1")

if st.button("Analyze PR"):
    if not repo_url:
        st.warning("Please enter a URL.")
    else:
        with st.spinner("🔍 Agents are reading the code... (this takes 5-10s)"):
            try:
                # Hit your local FastAPI backend
                response = requests.post(
                    "http://127.0.0.1:8000/analyze-pr", 
                    json={"repo_url": repo_url}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    comments = data.get("review_comments", [])
                    
                    if not comments:
                        st.success("✅ No issues found! Code looks clean.")
                    else:
                        st.subheader(f"Found {len(comments)} Issues")


                        for item in comments:
                            with st.expander(f"{item['type']}: {item['file']}"):
                                st.markdown(f"**Severity:** {item.get('type', 'General')}")
                                st.code(item['line'], language='python')
                                st.write(f"💡 **Suggestion:** {item['comment']}")
                else:
                    st.error(f"Error: {response.text}")
            
            except Exception as e:
                st.error(f"Connection Error. Is the backend running? {e}")

st.markdown("---")
st.caption("Created by rahulmani")