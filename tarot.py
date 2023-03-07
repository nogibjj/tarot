# write a tarot program that will read a tarot card from the user and print the meaning of the card

# define the main function
import pandas as pd
import matplotlib.pyplot as plt
import PIL
import datetime

data = pd.read_json('/workspaces/tarot/archive 2/tarot-images.json')
df = pd.json_normalize(data['cards'])

df['fortune_telling_1'] = df['fortune_telling'].str[0]
df['fortune_telling_2'] = df['fortune_telling'].str[1]
df['fortune_telling_3'] = df['fortune_telling'].str[2]

# # Learn infomation about the selected card
# def tarot_information(dataframe, card_num):
    
#     # identify images
#     name_img = dataframe['img'].iloc[card_num]
#     # open images
#     img = PIL.Image.open(f'/workspaces/tarot/archive 2/cards/{name_img}')
    
#     print('All the info you need for the {} card:'.format(dataframe['name'].iloc[card_num]))
    
#     plt.figure()
#     plt.title(dataframe['name'].iloc[card_num])
#     plt.imshow(img)
#     plt.axis('off')
#     plt.show()
    
#     print('Number: ')
#     print(dataframe['number'].iloc[card_num])
#     print('')
#     print('Arcana: ')
#     print(dataframe['arcana'].iloc[card_num])
#     print('')
#     print('Suit: ')
#     print(dataframe['suit'].iloc[card_num])
#     print('')
#     print('Numerology: ')
#     print(dataframe['Numerology'].iloc[card_num])
#     print('')
#     print('Element: ')
#     print(dataframe['Elemental'].iloc[card_num])
#     print('') 
#     if df.Astrology.notna().iloc[card_num] == True:
#         return 'Astrology'+ dataframe['Astrology'].iloc[card_num]

#     if df.Affirmation.notna().iloc[card_num] == True:
#         print('Affirmation')
#         return 'Affirmation:' + dataframe['Affirmation'].iloc[card_num]

def tarot_reading(dataframe):

    reading = dataframe.sample(n = 3).reset_index(drop=True)    
    today = datetime.date.today()
    date = today.strftime("%d-%B-%Y")
    
    # identify images
    name_img_past = reading['img'].iloc[0]
    name_img_present = reading['img'].iloc[1]
    name_img_future = reading['img'].iloc[2]

    # open images
    img_past = PIL.Image.open(f'/workspaces/tarot/archive 2/cards/{name_img_past}')
    img_present = PIL.Image.open(f'/workspaces/tarot/archive 2/cards/{name_img_present}')
    img_future = PIL.Image.open(f'/workspaces/tarot/archive 2/cards/{name_img_future}')
    # plot images
    fig, (past, present, future) = plt.subplots(1, 3, figsize=(10,5.5))
    fig.suptitle('Your reading: Past, Present, Future on {}'.format(date))
    past.imshow(img_past)
    past.axis('off')
    past.set_title(reading['name'].iloc[0])
    present.imshow(img_present)
    present.axis('off')
    present.set_title(reading['name'].iloc[1])
    future.imshow(img_future)
    future.axis('off')
    future.set_title(reading['name'].iloc[2])
    plt.show()

    # Outcomes
    print('My dearest, your fortune reading is about your past, present and future.')
    print('')
    print('Regarding your past: ')
    print(reading['fortune_telling_1'].iloc[0])
    print(reading['fortune_telling_2'].iloc[0])
    print(reading['fortune_telling_3'].iloc[0])
    print('')
    print('Regarding your present: ')
    print(reading['fortune_telling_1'].iloc[1])
    print(reading['fortune_telling_2'].iloc[1])
    print(reading['fortune_telling_3'].iloc[1])
    print('')
    print('Regarding your future: ')
    print(reading['fortune_telling_1'].iloc[2])
    print(reading['fortune_telling_2'].iloc[2])
    print(reading['fortune_telling_3'].iloc[2])

    #turn into a write streamlit function
    st.image(img_past, caption=reading['name'].iloc[0], use_column_width=True)
    st.write('Past: ')
    st.write(reading['fortune_telling_1'].iloc[0])
    st.write(reading['fortune_telling_2'].iloc[0])
    st.write(reading['fortune_telling_3'].iloc[0])
    st.image (img_present, caption=reading['name'].iloc[1], use_column_width=True)
    st.write('Present: ')
    st.write(reading['fortune_telling_1'].iloc[1])
    st.write(reading['fortune_telling_2'].iloc[1])
    st.write(reading['fortune_telling_3'].iloc[1])
    st.image(img_future, caption=reading['name'].iloc[2], use_column_width=True)
    st.write('Future: ')
    st.write(reading['fortune_telling_1'].iloc[2])
    st.write(reading['fortune_telling_2'].iloc[2])
    st.write(reading['fortune_telling_3'].iloc[2])

                

# create a web app that can record your daily tarot reading and save it to txt

import streamlit as st

def tarot_information(dataframe, card_num):
    
    # identify images
    name_img = dataframe['img'].iloc[card_num]
    # open images
    img = PIL.Image.open(f'/workspaces/tarot/archive 2/cards/{name_img}')
    
    st.write(f'All the info you need for the {dataframe["name"].iloc[card_num]} card:')
    
    st.image(img, caption=dataframe['name'].iloc[card_num], use_column_width=True)
    
    st.write('Number:')
    st.write(dataframe['number'].iloc[card_num])
    st.write('')
    st.write('Arcana:')
    st.write(dataframe['arcana'].iloc[card_num])
    st.write('')
    st.write('Suit:')
    st.write(dataframe['suit'].iloc[card_num])
    st.write('')
    st.write('Numerology:')
    st.write(dataframe['Numerology'].iloc[card_num])
    st.write('')
    st.write('Element:')
    st.write(dataframe['Elemental'].iloc[card_num])
    st.write('')
    if df.Astrology.notna().iloc[card_num] == True:
        st.write('Astrology')
        st.write(dataframe['Astrology'].iloc[card_num])

    if df.Affirmation.notna().iloc[card_num] == True:
        st.write('Affirmation')
        st.write(dataframe['Affirmation'].iloc[card_num])



st.title('Tarot Card Reading')
st.write('Welcome to the Tarot Card Reading App. Here you can learn about the meaning of a tarot card and get a daily reading.')

# create a sidebar
st.sidebar.title('Menu')

# # create a menu
menu = ['Learn about a card', 'Get a daily reading', 'my past notes']
choice = st.sidebar.selectbox('Menu', menu)

if choice == 'Learn about a card':
    st.subheader('Learn about a card')
    st.write('Here you can learn about a tarot card')
    # create a dropdown menu
    card = st.selectbox('Select a card', df['name'])
    # create a button to get information
    if st.button('Get information'):
        # get the index of the card
        card_num = df[df['name'] == card].index[0]
        # call the function
        tarot_information(df, card_num)
        st.success('Information saved')

elif choice == 'Get a daily reading':
    st.subheader('Get a daily reading')
    st.write('Here you can get a daily reading')
    # create a button to get a reading
    if st.button('Get a reading'):
        # call the function
        tarot_reading(df)
        st.success('Reading saved')


st.sidebar.subheader('About')
st.sidebar.text('This app was created by Emma Wang')
