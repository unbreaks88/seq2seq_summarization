import csv
import re
import time

from konlpy.tag import Mecab

banned_tag = {'SF': 'SF',
              'SE': 'SE',
              'SSO': 'SSO',
              'SSC': 'SSC',
              'SC': 'SC',
              'SY': 'SY'
              # 'JKS': 'JKS',
              # 'JKC': 'JKC',
              # 'JKG': 'JKG',
              # 'JKO': 'JKO',
              # 'JKB': 'JKB',
              # 'JKV': 'JKV',
              # 'JKQ': 'JKQ',
              # 'JX': 'JX',
              # 'JC': 'JC'
              }

mecab = Mecab('/usr/local/lib/mecab/dic/mecab-ko-dic')

stopwords = set()


def load_stopwords(path):
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for stopword in lines:
            stopwords.add(stopword)

# def tokenize(sentences):
#     tokenized_sentences = []
#
#     for sentence in sentences:
#         tokens = mecab.pos(''.join(sentence), flatten=False)
#
#         for token in tokens:
#             new_tokens = []
#             for _token in token:
#                 if not _token[1] in banned_tag:
#                     new_tokens.append(_token[0])
#             tokenized_sentences.append(new_tokens)
#     return tokenized_sentences


def tokenize(sentences):
    tokenizing_sentences = []

    for sentence in sentences:
        # tokens = mecab.pos(''.join(sentence))
        tokens = mecab.morphs(''.join(sentence))
        # tokens = mecab.nouns(''.join(sentence))
        new_tokens = []
        for token in tokens:
            if not token[1] in banned_tag and token[0] not in stopwords:
                new_tokens.append(token[0])
        tokenizing_sentences.append(new_tokens)
    return tokenizing_sentences


def separate_sentences(*delimiters):
    return lambda value: re.split('|'.join([re.escape(delimiter) for delimiter in delimiters]), value)


def clean_data(filename):
    file = open(filename, 'r', encoding='utf-8')
    lines = csv.reader(file, delimiter='\t')

    results = []

    print('before make_train_data')
    start_time = time.time()
    for idx, line in enumerate(lines):
        if (idx % 1000) == 0:
            print('step: {}, time: {:f}'.format(idx, (time.time() - start_time)))
            start_time = time.time()

        if len(line) == 5:
            temp_summary_list = line[4].splitlines()
            summaries = ''.join([summary.strip() for summary in temp_summary_list])
            category = line[1].strip()
            contents = separate_sentences('. ', '? ', '! ', '\n', '.\n')(''.join(line[3].splitlines()))

            if len(contents) > 2:
                contents = contents[:2]
                if len(contents[0]) < 8:
                    continue
            contents = ' '.join(content.strip() for content in contents)

            # p = re.compile('\【.*?\=')

            p = re.compile('\<.*?\>')
            contents = re.sub(p, "", contents)
            summaries = re.sub(p, "", summaries)
            p = re.compile('\[.*?\]')
            contents = re.sub(p, "", contents)
            summaries = re.sub(p, "", summaries)
            p = re.compile('\【.*?\】')
            contents = re.sub(p, "", contents)
            summaries = re.sub(p, "", summaries)
            p = re.compile('\(.*?\)')
            summaries = re.sub(p, "", summaries)
            contents = re.sub(p, "", contents)
            p = re.compile('.*?\ 기자 =')
            contents = re.sub(p, "", contents)
            contents = re.sub(p, "", contents)
            # summaries = re.sub('[-=.#/?:$}]', '', summaries).strip()
            contents = re.sub('[-=.#/?:$}◆⑤]', '', contents).strip()
            contents = re.sub('사진뉴스1', '', contents).strip()

            contents = separate_sentences('. ', '? ', '! ', '\n', '.\n')(''.join(contents))
            contents = ' '.join(content.strip() for content in contents)

            # if summaries.__contains__('[') or summaries.__contains__('(') or summaries.__contains__('<') or summaries.__contains__(
            #         '→') or summaries.__contains__('↓') or summaries.__contains__('↑'):
            #     continue
            if contents.__contains__('[') or contents.__contains__('(') or contents.__contains__(
                    '<') or contents.__contains__('#') or contents.__contains__('◀') or contents.__contains__(
                '【') or contents.__contains__('@'):
                continue

            results.append([summaries, contents, (category + ', ' + contents)])

    return results
    print('after make_train_data')

def test(contents):
    p = re.compile('\<.*?\>')
    contents = re.sub(p, '', contents)
    p = re.compile('\[.*?\]')
    contents = re.sub(p, '', contents)

    p = re.compile('\【.*?\】')
    contents = re.sub(p, '', contents)

    p = re.compile('\(.*?\)')
    contents = re.sub(p, '', contents)
    return contents


if __name__ == '__main__':

    dd = '사조화인코리아 도축장도 AI 검출..전남 일시 이동중지(종합) 전남 지역 농가에서 고병원성 조류인플루엔자(AI)가 잇따라 발생한 가운데 계열화사업자 \'사조화인코리아\'에 소속된 오리 도축>장에서도 H5형 AI 바이러스가 검출됐다. 방역당국은 전남 전 지역과 사조화인코리아 소속 모든 계열농장·도축장 등에 대해 일시 이동중지 명령을 발령했다. 농림축산식품부는 전남 고흥에 있는 육용오리 농장(8천300수 규모)에서 나주 소재 사조화인     코리아 오리도축장으로 출하된 오리에 대한 검사 결과 H5형 AI가 확인됐다고 1일 밝혔다. 농식품부는 지난달 9일 이후 오리 도축장에 대한 AI 검사를 강화해 실시하고 있으며, 이번 농장 역시 도축장 검사 과정에서 바이러스가 확인됐다. 고병원성 >     여부는 이르면 이틀 안에 판명될 전망이다. 농식품부는 전남에 오염원이 상당 부분 퍼져 있다고 보고 전남 전 지역과 사조화인코리아에 소속된 전국 모든 농가에 대해 2일 0시부터 24시간 동안 일시 이동중지 명령을 발동했다. 일시 이동중지 적용대상은 국가동물방역통합시스템(KAHIS)에 등록된 약 1만4천 개소다. 구체적으로 전남 지역에서는 가금농가 8천138개소, 도축장 10개소, 사료공장 23개소, 차량 6천80대, 사조화인코리아 소속 가금농가 137개소(전남 113, 전북 22, 경기 1, 경남 1), 도축장 4(전남 2, 전북 2), 부화장 6(전남 4, 충남 1, 경기 1), 차량 83대 등이다. 농식품부는 이와 함께 AI 항원 검출 직후 해당 도축장을 폐쇄하고, 도축장 내 해당 발생농가와 함께 도축된 오리(3농가 3만6천700수) 지육을 전량 폐기했다. 이에 따>     라 해당 발생농가와 함께 계류·도축된 오리 및 지육의 외부 반출 물량은 없다고 농식품부는 설명했다. 또 중앙기동방역기구 및 중앙역학조사반을 현장에 급히 파견해 현장 차단방역 조치와 역학조사를 실시하고 있다. 해당 도축장으로 오리를 출하한 농가의 경우 지난달 26일 고병원성 AI가 발생한 고흥 육용오리 농가 방역대(3㎞ 이내) 안에 있어 이미 이동통제가 이뤄지고 있었다고 농식품부는 설명했다. 농식품부 관계자는 "AI의 추가 확산을 막기 위해 가금농가 및 철새도래지 방문 자제, 의사 환축 발생지역 이동통제 및 소독 등의 차단방역 조치에 가금사육 농가는 물론 국민들도 적극적으로 협조해달라\"고 당부했다.'
    test(dd)

    # file_name = '/Users/unbreaks/git/seq2seq_summarization/crawler/test_data/20180521.csv'
    # results = clean_data(file_name)
    # after_results = make_train_data(results)

    load_stopwords('/Users/unbreaks/git/seq2seq_summarization/utils/resources/stopwords.dic')

    # for result in results:
    #     result.pop(1)
    #     result.pop(1)
    #     result.pop(0)

    test = ['피겨여왕 김연아가 지난해 4월18일 오전 서울 종로구 SK 텔레콤 종각 T월드점에서 열린 \'갤럭시S8, S8+ 사전 개통 행사\'에서 1호 개통 고객인 김영범씨와 SKT에       서 개발 중인 자율주행차를 배경으로 기념촬영을 하고 있다 사진뉴스1']

    # results = [['MPC 직무교육 받는 자원봉사자들  연합뉴스                                          국내외 언론사가 입주한 평창동계올림픽 메인프레스센터가 때아닌 물난리      를 겪고 있다 올림픽 개막을 13일 앞둔 27일 주관통신사 연합뉴스와 로이터, AP통신 등 해외 통신사가 입주한 MPC3 천장에서 물이 떨어지기 시작했다']]
    results = [test]
    tokenizing_sentences = tokenize(results)
    print('result: {}'.format(results))
    print('tokenizing_sentences: {}'.format(tokenizing_sentences))
