import streamlit as st
import pandas as pd
from Task3 import BloomFilter, realQuery, Flajolet_Martin, realCount


data_bloomfilter = pd.read_csv('data/codon_usage.csv', dtype={"SpeciesID": 'Int64'})["SpeciesID"]
data_distinct_count = pd.read_csv('data/codon_usage.csv')["Kingdom"]


st.markdown("# Task 3 - Implementation of Bloom Filter and Flajolet-Martin algorithm")
st.markdown("# Bloom Filter")
n = st.number_input("Lenght of Bloom Filter", min_value=1, value=40000)
k = st.slider('Number of Hash Functions', min_value=1, max_value=8)
bloomfilter = BloomFilter(n, k, data_bloomfilter)

query_key = st.number_input("Query key", min_value=0)
result_bloomfilter = bloomfilter.queryKey(query_key)
real_result = realQuery(data_bloomfilter, query_key)

if result_bloomfilter == True and real_result == True:
    st.write(str(query_key) + " is a true positive")
elif result_bloomfilter == False and real_result == False:
    st.write(str(query_key) + " is a true negative")
elif result_bloomfilter == True and real_result == False:
    st.write(str(query_key) + " is a false positive")
st.write("Result bloomfilter: ", result_bloomfilter)
st.write("Real result: ", real_result)

st.markdown("# Count distinct")
fm_count = Flajolet_Martin(data_distinct_count)
real_count = realCount(data_distinct_count)
st.write("Count obtained by the Flajolet-Martin algorithm: ", fm_count)
st.write("Real count of distinct values ", real_count)
