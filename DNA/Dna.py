import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image

# DNA Image
image = Image.open('/Users/mac/Code/Python Projects/DNA/dna-logo.jpg')
st.image(image, use_container_width=True)

# Title
st.write("""
    # DNA Nucleotide Count Web App
    This app counts the nucleotide composition of query DNA!
***
""")

# Input Text Box
st.header('Enter DNA Sequence')
sequence_input = ">DNA Query 2\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

sequence = st.text_area("Sequence input", sequence_input, height=150)
sequence = sequence.splitlines()
sequence = sequence[1:]
sequence = ''.join(sequence)

st.write(''' 
    ***
''')

# Print the DNA sequence
st.header('Input DNA Query')
sequence

# DNA Nucleotide count
st.header("Output (DNA Nucleotide count)")

### 1. Print dictionary
st.subheader("1. Print dictionary")
def DNA_nucleotide_count(seq):
    d = dict([
            ('A', seq.count('A')),
            ('T', seq.count('T')),
            ('G', seq.count('G')),
            ('C', seq.count('C'))
        ])
    return d

X = DNA_nucleotide_count(sequence)

X

### 2. Print Text
st.subheader("2. Print Text")
st.write('There are ' + str(X['A']) + ' adenine (A)')
st.write('There are ' + str(X['T']) + ' thymine (T)')
st.write('There are ' + str(X['G']) + ' guanine (G)')
st.write('There are ' + str(X['C']) + ' cytosine (C)')

### 3. Display DataFrame
st.subheader("3. Display DataFrame")
df = pd.DataFrame.from_dict(X, orient='index')
df = df.rename({0: 'count'}, axis='columns')
df.reset_index(inplace=True)
df = df.rename(columns={'index': 'nucleotide'})
st.write(df)

### 4. Display Bar Chart Using Altair
st.subheader("4. Display Bar Chart")
p = alt.Chart(df).mark_bar().encode(
    x='nucleotide',
    y='count'
)
p = p.properties(width=alt.Step(80))
st.write(p)