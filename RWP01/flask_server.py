from flask import Flask, render_template , request
import pymysql
app=Flask(__name__)

#루트디렉토리
@app.route('/')
def main():
    return render_template('main.html') #main.html에서 실행 -> main에 입력받은데이터 -> search()에서 실행

@app.route('/search', methods=['POST', 'GET'])
def search():
    #post방식
    #select 이름 : 시군구(sigungu), 거래구분(trade_rent),  건물구분(buildings)
    # 시군구 선택옵션이름: choice_sigungu
    # 거래구분 선택옵션이름: choice_buyer
    # 건물구분 선택옵션이름: choice_building
    sigungu= request.form['sigungu']
    trade_rent=request.form['trade_rent']
    buildings=request.form['buildings']

    #데이터베이스 연결
    conn=pymysql.connect(host='localhost', user='root', password='1234', db='ekdb', charset='utf8')
    #cursor 생성
    curs=conn.cursor(pymysql.cursors.DictCursor)
    
    select_query= 'SELECT * FROM HOUSE_INFO WHERE 시=%s AND 거래구분=%s AND  건물구분=%s'
    curs.execute(select_query, (sigungu, trade_rent, buildings))
    conn.commit()

    # 검색 결과
    results=curs.fetchall()

    # 검색결과를 테이블로 나타내고, 검색결과 레코드 개수를 딕셔너리로 묶어서 result_page.html 로 전달
    templateData={ 'results': results, \
                   'result_len': len(results), \
                   'columns': ['ID', '행정구역', '시', '동', '도로명주소', '건물구분', '거래구분', '층', '계약년도', '계약월', '계약일', '매매가', '전세보증금', '월세'],\
                   'sigungu':sigungu, \
                   'trade_rent': trade_rent, \
                   'buildings': buildings }
    return render_template('result_page.html', **templateData)    
if __name__=='__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)
