import pandas as pd
from sqlalchemy import create_engine



# Opening csv with stats and saving as a database
college_df = pd.read_csv('college_df_with_scores.csv')
engine = create_engine('sqlite://', echo=False)
college_df.to_sql(name='players',con=engine)