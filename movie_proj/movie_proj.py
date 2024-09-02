import pandas as pd
import numpy as np
import seaborn as sns
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
import matplotlib.pyplot as plt



#%% TOP 15 movie
def top15():
    md =pd.read_csv('data/tmdb_5000_movies.csv')
    md['year'] = pd.to_datetime(md['release_date'], errors='coerce').apply(lambda x: str(x).split('-')[0] if x != np.nan else np.nan)
    vote_counts = md[md['vote_count'].notnull()]['vote_count']
    m = vote_counts.quantile(0.95)
    qualified = md[(md['vote_count'] >= m) & (md['vote_count'].notnull()) & (md['vote_average'].notnull())][['title', 'year', 'vote_count', 'vote_average', 'popularity', 'genres']]
    top15 = qualified[['title','vote_average','year']].head(15)
    top15_reset=top15.reset_index(drop=True)
    top15_reset.index = top15_reset.index+1
    print(top15_reset)
    print('-'*50)
    return top15_reset

#%% 시각화

def plot():
    print('장르별 선호도(평점순 상위 100개 항목)')
    plt.rc('font', family='Malgun Gothic')
    
    md =pd.read_csv('data/tmdb_5000_movies.csv')
    md['year'] = pd.to_datetime(md['release_date'], errors='coerce').apply(lambda x: str(x).split('-')[0] if x != np.nan else np.nan)
    md['genres'] = md['genres'].fillna('[]').apply(literal_eval).apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
    vote_counts = md[md['vote_count'].notnull()]['vote_count']
    m = vote_counts.quantile(0.95)
    vote_averages = md[md['vote_average'].notnull()]['vote_average']
    C = vote_averages.mean()
    qualified = md[(md['vote_count'] >= m) & (md['vote_count'].notnull()) & (md['vote_average'].notnull())][['title', 'year', 'vote_count', 'vote_average', 'popularity', 'genres']]
    qualified['wr'] = qualified.apply(lambda x: (x['vote_count']/(x['vote_count']+m) * x['vote_average']) + (m/(m+x['vote_count']) * C), axis=1)
    qualified = qualified.sort_values('wr', ascending=False).head(250)
    cz = qualified.head(100)
    sq = cz.apply(lambda x: pd.Series(x['genres']), axis=1).stack().reset_index(level=1, drop=True)
    sq.name ='genre'
    gen_cz = cz.drop('genres', axis=1).join(sq)
    gen_cz["genre"].value_counts().sort_index()
    sns.countplot(y="genre",data= gen_cz,order = gen_cz["genre"].value_counts().index)
    scp = sns.countplot(y="genre",data= gen_cz,order = gen_cz["genre"].value_counts().index).set_title("장르별 선호도(평점순 상위 100개 항목)")
    return scp
    
#%% 장르 검색
def build_chart(genre, percentile=0.85):
    md =pd.read_csv('data/tmdb_5000_movies.csv')
    md['year'] = pd.to_datetime(md['release_date'], errors='coerce').apply(lambda x: str(x).split('-')[0] if x != np.nan else np.nan)
    md['genres'] = md['genres'].fillna('[]').apply(literal_eval).apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])
    s = md.apply(lambda x: pd.Series(x['genres']), axis=1).stack().reset_index(drop=True)
    s.name = 'genre'
    gen_md = md.drop('genres', axis=1).join(s)
    md2 = gen_md[gen_md['genre'].str.contains(genre,case=False,na=False)]
    md2 = md2.drop_duplicates(['genre'])
    md2 = md2.reset_index()
    md2.index = md2.index+1
    print(md2[['genre']])
    mvse = int(input('원하는 장르의 숫자를 선택해주세요 : '))
    mv2 = md2.iloc[mvse-1]
    df = gen_md[gen_md['genre'] == mv2['genre']]
    
    vote_counts = df[df['vote_count'].notnull()]['vote_count']
    vote_averages = df[df['vote_average'].notnull()]['vote_average']
    C = vote_averages.mean()
    m = vote_counts.quantile(percentile)
        
    qualified = df[(df['vote_count'] >= m) & (df['vote_count'].notnull()) & (df['vote_average'].notnull())][['title','year','vote_count','vote_average','popularity']]
        
    qualified['wr'] = qualified.apply(lambda x: (x['vote_count']/(x['vote_count']+m) * x['vote_average']) + (m/(m+x['vote_count']) * C), axis=1)
    qualified = qualified.sort_values('wr', ascending=False).head(250)
    top15 = qualified[['title','vote_average','year']].head(15)
    top15_reset=top15.reset_index(drop=True)
    top15_reset.index = top15_reset.index+1
    print(top15_reset)
    print('-'*50)
    return top15_reset
#%%
def improved_recommendations(title):
    md =pd.read_csv('data/tmdb_5000_movies.csv')
    md['year'] = pd.to_datetime(md['release_date'], errors='coerce').apply(lambda x: str(x).split('-')[0] if x != np.nan else np.nan)
    md['tagline'] = md['tagline'].fillna('')
    md['description'] = md['overview'] + md['tagline']
    md['description'] = md['description'].fillna('')
    
    tf = TfidfVectorizer(analyzer='word', ngram_range=(1, 2), min_df=0, stop_words='english')
    tfidf_matrix = tf.fit_transform(md['description'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    
    indices = pd.Series(md.index, index=md['title'])
    
    md2 = md[md['title'].str.contains(title,case=False)]
    md2 = md2.reset_index()
    md2.index = md2.index+1
    print(md2[['title']])
    mvse = int(input('원하는 영화의 숫자를 선택해주세요 : '))
    mv2 = md2.iloc[mvse-1]
    idx = indices[mv2['title']]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:26]
    movie_indices = [i[0] for i in sim_scores]

    movies = md.iloc[movie_indices][['title','vote_count','vote_average','year']]
    
    vote_counts = movies[movies['vote_count'].notnull()]['vote_count']
    m = vote_counts.quantile(0.60)
    vote_averages = md[md['vote_average'].notnull()]['vote_average']
    C = vote_averages.mean()
    qualified = movies[(movies['vote_count'] >= m) & (movies['vote_count'].notnull())].copy()
    qualified['wr'] = qualified.apply(lambda x: (x['vote_count']/(x['vote_count']+m) * x['vote_average']) + (m/(m+x['vote_count']) * C), axis=1)
    qualified = qualified.sort_values('wr', ascending=False).head(10)
    top10 = qualified[['title','vote_average','year']]
    top10_reset=top10.reset_index(drop=True)
    top10_reset.index = top10_reset.index+1
    print(top10_reset)
    print('-'*50)
    return top10_reset

#영화 찾기
def movie_search(input_title):
    md =pd.read_csv('data/tmdb_5000_movies.csv')
    md['year'] = pd.to_datetime(md['release_date'], errors='coerce').apply(lambda x: str(x).split('-')[0] if x != np.nan else np.nan)
    vote_counts = md[md['vote_count'].notnull()]['vote_count']
    vote_averages = md[md['vote_average'].notnull()]['vote_average']
    C = vote_averages.mean()
    m = vote_counts.quantile(0.60)  
    md['wr'] = md.apply(lambda x: (x['vote_count']/(x['vote_count']+m) * x['vote_average']) + (m/(m+x['vote_count']) * C), axis=1)
    md2 = md[md['title'].str.contains(input_title,case=False)].sort_values('wr',ascending=False) #
    md2 = md2.reset_index()
    md2.index = md2.index+1
    print(md2[['title','vote_average','year']])
    print('-'*50)
    return md2[['title','vote_average','year']]

    #영화 상세 메뉴
def movie_menu():
    while True:
        print('-'*50)
        print('1.TOP15 2.영화 찾기 3.장르 추천 4.영화 추천 5.장르별 선호도 6.나가기')
        print('-'*50)
        m = input()
        if m == '1':
            top15()
        elif m == '2':
            movie_search(input('영화 제목을 입력하시오: '))
        elif m == '3':
            build_chart(input('영화 장르를 입력해주세요: ')) 
        elif m == '4':
            improved_recommendations(input('영화제목을 입력해주세요 : '))
        elif m == '5':
            plot()
            
        elif m == '6':
            break
        
        
