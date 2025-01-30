import streamlit as st
import sqlite3
from datetime import datetime


# 데이터 저장 함수
def save_to_db(quotes):
    conn = sqlite3.connect('quotes.db')
    c = conn.cursor()

    #quotes = input("명언을 입력하세요: ")
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute("INSERT INTO quotes_test (quotes, created_at) VALUES (?, ?)", (quotes, created_at))
    conn.commit()
    conn.close()
 

# 데이터 조회 함수
def get_all_entries():
    conn = sqlite3.connect('quotes.db')
    c = conn.cursor()
    c.execute("SELECT quotes, created_at FROM quotes_test ORDER BY created_at DESC")
    data = c.fetchall()
    #print(data)
    conn.close()
    return data


# 앱 메인 화면 구성
def main():
    st.title("📝 명언제조기")
    
     # 입력 폼 생성
    with st.form("entry_form"):
        quotes = st.text_input("명언을 입력하세요")        
        submitted = st.form_submit_button("저장하기")

        if submitted:
            if quotes:
                save_to_db(quotes)
                st.success("✅ 명언이 성공적으로 저장되었습니다!")
            else:
                st.warning("⚠️ 다시 입력해주세요!")

    # 저장된 데이터 표시
    st.subheader("저장된 명언들")
    entries = get_all_entries()
    
    if entries:
        # 데이터프레임으로 변환
        entries_df = st.dataframe(
            entries,
            column_config={
                "0": "내용",
                "1": "등록일시"
            },
            hide_index=True
        )
    else:
        st.info("📭 아직 저장된 데이터가 없습니다.")

if __name__ == "__main__":
    main()
