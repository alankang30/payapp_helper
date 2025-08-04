import streamlit as st
import numpy as np
import pandas as pd

st.header("Charlie's Super PayApp Helper")
'''
Created by Alan Kang (Unless it doesn't work, in which case it was created by Ike Case)
'''
st.image("./charlie.png", use_container_width=True)
file = st.file_uploader("Upload a Monthly Cost Detail Report")
keyFile = st.file_uploader("Upload a Key")

codeToName = {}
lineItems = []

if keyFile is not None:
    keyDf = pd.read_excel(keyFile, sheet_name='Sheet1')

    melted = keyDf.melt(id_vars='Name', value_name='Code').dropna(subset=['Code'])
    final_df = melted[['Code', 'Name']].reset_index(drop=True)
    #st.table(final_df)

    codeToName = dict(zip(final_df['Code'], final_df['Name']))

    lineItems = [(name, []) for name in final_df['Name'].unique()]

    #print(lineItems)
    


if file is not None and keyFile is not None:
    df = pd.read_excel(file, sheet_name='Sheet1')

# Assuming df has already been cleaned and columns renamed
# and we're working with the first 9 columns only

    condition = (
        df.iloc[:, 0].isna() &              # column 1
        #df.iloc[:, 2].isna() &              # column 3
        df.iloc[:, 3].isna() &              # column 4
        df.iloc[:, 4].isna() &              # column 5
        df.iloc[:, 5].isna() &              # column 6
        df.iloc[:, 6].isna() &              # column 7
        df.iloc[:, 7].isna() &              # column 8
        #df.iloc[:, 1].notna() &             # column 2
        df.iloc[:, 8].notna() &              # column 9
        (df.iloc[:, 1].notna() |  df.iloc[:, 2].notna()) # either or
    )

    df = df[condition].reset_index(drop=True).filter(['Unnamed: 1', 'Unnamed: 2', 'Unnamed: 8'])

    array = df.fillna('NaN').values


    for i in range(0, len(array), 1):
        idx = len(array) - 1 - i
        if array[idx][0] == 'NaN':
            array[idx][0] = last_val
        else:
            last_val = array[idx][0]
            array[idx][0] = None

    cost_detail_items = []
    for row in array:
        if row[0] is not None:
            cost_detail_items.append(row)
    



    #st.table(pd.DataFrame(cost_detail_items))

    misc = []
    for item in cost_detail_items:
        code = item[0].split('--')[0].replace('-', '.')

        if item[1][0:2] == 'OE':
            code = code + '.' + item[1][0:2]
        else:
            code = code + '.' + item[1][0:1]
        #print('CODE', code)


        try:
            name = codeToName[code]
        except:
            misc.append((code, item[0].split('--')[1], item[1], item[2]))
            continue



        for lineItem in lineItems:
            if lineItem[0] == name:
                print(code, 'is under', lineItem)
                if lineItem[1] is None:
                    lineItem[1] = []
                else:
                    lineItem[1].append(item)
                break

    print('misc:',misc)

    st.header('PayApp breakdown')

    super_total =0

    for lineItem in lineItems:
        description_work = lineItem[0]
        st.subheader(description_work)

        total = 0
        detail_items = lineItem[1]
        for detail_item in detail_items:
            total += detail_item[2]
        st.write(f'Total:  ${total:.2f}')
        super_total += total

        st.dataframe(pd.DataFrame(detail_items), column_config={1:st.column_config.Column("Cost Detail Item"), 
                                                                2:st.column_config.Column("Type"), 
                                                                3:st.column_config.NumberColumn("Amount ($)", format="%.2f")}
                                                                )


    st.write('PayApp Total for this month:', super_total)

    # MISC
    st.header("Cost Detail Items missing a key", divider="red")
    st.dataframe(pd.DataFrame(misc), column_config={1:st.column_config.Column("Cost Code (Copy into key file)", width="medium"), 
                                                    2:st.column_config.Column("Cost Detail Item"),
                                                    3:st.column_config.Column("Type"), 
                                                    4:st.column_config.NumberColumn("Amount ($)", format="%.2f")}
                                                    )























# st.button("Click me")
# #st.download_button("Download file", data)
# st.link_button("Go to gallery", "https://thecubicle.us")
# #st.page_link("page.py", label="Home")
# st.checkbox("I agree")
# st.feedback("thumbs")
# st.pills("Tags", ["Sports", "Politics"])
# st.radio("Pick one", ["cats", "dogs"])
# st.segmented_control("Filter", ["Open", "Closed"])
# st.toggle("Enable")
# st.selectbox("Pick one", ["cats", "dogs"])
# selections = st.multiselect("Buy", ["milk", "apples", "potatoes"])
# print(selections.__class__)
# print(selections)
# st.slider("Pick a number", 0, 100)
# st.select_slider("Pick a size", ["S", "M", "L"])
# st.text_input("First name")
# st.number_input("Pick a number", 0, 10)
# st.text_area("Text to translate")
# st.date_input("Your birthday")
# st.time_input("Meeting time")

# st.audio_input("Record a voice message")
# st.camera_input("Take a picture")
# st.color_picker("Pick a color")

# Insert a chat message container.
# with st.chat_message("user"):
#     st.write("Hello 👋")
#     st.line_chart(np.random.randn(30, 1))

# msgs = []

# # Display a chat input widget at the bottom of the app.



# # Display a chat input widget inline.
# with st.container():
#     msgs.append(st.chat_input("Say something"))

# if msgs[-1]:
#     with st.chat_message("user"):
#         st.write(msgs[-1])
#     with st.chat_message("assistant"):
#         st.write("Hello!")