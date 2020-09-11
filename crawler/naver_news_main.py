import sys
from collections import Counter
from pprint import pprint
from itertools import chain

from direct_redis import DirectRedis

from config_setting.config_redis import RedisConfig
from corpus.corpus.naver_api import NaverNewsSearch
from corpus.corpus.tokenizers import KoreanTokenizer, get_nfc_text


def set_query_result(query, max_len=1000):
    if r.hexists('naver-news-lists', query):
        texts = [news.get('body') for news in r.hget('naver-news-lists', query)]
        texts = [get_nfc_text(text) for text in texts]
        tokens = [tok.pos(text) for text in texts]
        tokens_agg = chain.from_iterable(tokens)
    else:
        responses = news_search.get_news(query, max_len=max_len)
        newslist = []
        texts_agg, tokens_agg = [], []
        for res in responses:
            if res['link'].startswith("https://news.naver.com"):
                try:
                    body_text = news_search.get_naver_news_body(res['link'])
                    body_text = get_nfc_text(body_text)
                    tokens = tok.pos(body_text)
                    res['body'] = body_text
                    res['tokens'] = tokens
                    newslist.append(res)
                    texts_agg.append(body_text)
                    tokens_agg += tokens
                except Exception as e:
                    print(e)
        print(f"number of retrieved news: {len(newslist)}")
        overwrite_redis_hash(r, 'naver-news-lists', query, newslist)

    tokens_count = Counter(tokens_agg).most_common(1000)
    overwrite_redis_hash(r, 'naver-news-counts', query, tokens_count)

    print(query)
    pprint(tokens_count[:10])


def overwrite_redis_hash(r: DirectRedis, field, key, value):
    if r.hexists(field, key):
        print(f"key {key} exsists, delete the key")
        r.hdel(field, key)
    r.hset(field, key, value)


def main():
    queries = ['석유', '원유', '천연가스', '셰일가스', '시추', '정유', '석탄', '우라늄', '에너지', '나프타', '합성섬유', '나일론', '폴리에스터', '아크릴', '탄소섬유', '타이어', '라텍스', '카본블랙', '비료', '농약', '탄산가스', '스티로폴', '필름', '페인트', '플라스틱', '도료', '안료', '폭발물', '살충제', '접착제', '코팅제', '모래', '점토', '석고', '석회', '골재', '시멘트', '콘크리트', '벽돌', '금속용기', '유리용기', '플라스틱용기', '병마개', '종이', '포장지', '보드지', '알루미늄', '채광', '광산', '보크사이트', '구리', '금속용기', '귀금속', '백금', '다이아몬드', '희토류', '은', '철강', '임산물', '목재', '건축용 판재', '우주항공', '국방', '방산', '건축', '건설', '토목공학', '전기 부품', '전기 케이블', '전선', '중전기', '발전 터빈', '발전 장비', '건설장비', '트럭', '토공 장비', '트랙터', '송풍기', '프레스', '머신툴', '압축기', '엘리베이터', '에스컬레이터', '절연체', '펌프', '롤러 베어링', '무역', '인쇄', '폐기물', '오염 통제', '사무 서비스', '사무용품', '청소 서비스', '케이터링', '장비 수리', '직업 소개소', '직원 훈련', '인력 파견', '교정 시설', '보안 서비스', '경보 서비스', '경호', '무장 수송', '리서치', '컨설팅', '마케팅', '항공 운송', '항공 물류', '항공 택배', '항공사', '해운회사', '철도회사', '육상 운송', '차량 렌탈', '택시', '공항 서비스', '공항', '고속도로', '선로', '항구', '자동차 부품', '자동차 부품', '오토바이', '타이어', '고무', '가전제품', 'TV', '오디오', '게임 콘솔', '디지털 카메라', '카펫', '벽지', '쇼파', '침대', '주택 건설', '조립식 주택', '가정용 기기', '가정용품', '요리도구', '유리 그릇', '크리스탈식기', '은식기', '부엌용품', '소비자용품', '스포츠 장비', '자전거', '장난감', '의류', '액세사리', '사치품', '핸드백', '지갑', '가방', '보석', '시계', '신발', '운동화', '가죽 신발', '섬유', '면', '폴리에스테르', '모', '캐시미어', '카지노', '복권', '베팅', '호텔', '리조트', '크루즈', '스포츠 센터', '피트니스 센터', '경기장', '골프장', '놀이공원', '워터파크', '레스토랑', '바', '술집', '패스트푸드', '교육', '세미나', '교재', '주거 서비스', '가정 보안', '법률 서비스', '개인 서비스', '인테리어 디자인', '소비자 경매', '결혼식', '장례식', '도매업체', '자동차 대리점', '인터넷 소매', '홈쇼핑', '백화점', '컴퓨터', '서점', '자동차 딜러', '주유소', '약국', '재래시장', '하이퍼마켓', '대형 쇼핑센터', '맥주', '증류업체', '양조업체', '청량음료', '농산물', '유제품', '과일 주스', '고기', '가금류', '생선', '애완동물 음식', '담배', '세제', '비누', '기저귀', '화장품', '향수', '의료기기', '약물전달 장치', '진단장비', '주사기', '병원', '요양원', '재활 센터', '동물 병원', 'HMO', '생명공학', '제약', '임상시험', '은행', '모기지', '핀테크', '신용 카드', '리스 금융', '현금 서비스', '전당포', '유가증권', '뮤추얼 펀드', '폐쇄형 펀드', '개방형 펀드', '유닛 트러스트', '재무 자문', '보험', '재보험', '금융상품', '파생상품', '신용평가', '생명보험', '건강보험', '화재보험', '손해보험', '정보 기술 컨설팅', '백오피스', '클라우드', '데이터 센터', '애플리케이션', '어플', '데이터베이스', '소프트웨어', '통신 장비', 'LAN', 'WAN', '라우터', '전화기', '스위치보드', '휴대폰', 'PC', '서버', '컴퓨터 부품', '컴퓨터 주변기기', '모니터', '키보드', '프린터', '스캐너', '바코드', '레이저', 'POS 기계', '콘덴서', '전자 코일', '인쇄 회로 기판', '변압기', '하드웨어', '반도체 장비', '반도체 장비', '고 대역폭 케이블', '광섬유 케이블', '유선 통신 서비스', '무선 통신 서비스', '인터넷 서비스', '셀룰러 서비스', '광고', '홍보', '방송', '라디오', '케이블', '위성 TV', '출판', '인쇄물', '신문', '잡지', '책', '영화', 'TV쇼', '예능', '극장', '스포츠팀', '교육용 소프트웨어', '모바일 게임', '플랫폼', '검색엔진', '소셜미디어', '네트워크 플랫폼', '발전소', '가스공사', '원자력 발전소', '원전', '수도', '태양열 발전', '수력발전', '풍력발전', '부동산 운영', '부동산 관리', '부동산 개발', '부동산 중개', '리츠']
    # queries = ['현대중공업']
    for query in queries:
        set_query_result(query, 1000)


if __name__ == '__main__':
    tokenizer_name = sys.argv[1] if sys.argv[1] else None
    if tokenizer_name in KoreanTokenizer.toks.keys():
        tok = KoreanTokenizer(tokenizer_name)
        RedisConfig.DEV_DEPL_choice = 'DEPL'
        r = DirectRedis(**RedisConfig.REDIS_INFO.get('naver-news'))
        news_search = NaverNewsSearch()
        print(tokenizer_name, tok)
    else:
        raise Exception("Wrong Tokenizer Name")

    main()
