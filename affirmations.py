import random
from deepface import DeepFace

# DeepFace analyze emotion
img_path = "input_image.jpg"
emotion = DeepFace.analyze(img_path = img_path, actions = ['emotion'])

#return affirmations based on emotion detected using pre-made text
#emotions:  Neutral, Happy, Sad, Angry, Disgust, Surprise

# affirmations 
neutral_affirmation = ['Today will be a good day', 'I am allowed to rest.', ]
happy_affirmation = ['I am filled with so much energy and joy.', 'Expressing this joy is my right.', 'I deserve to live a happy and healthy life.',
'I no longer wait for something bad to ruin my happiness.', 'I create my own version of happiness every day.', 'I choose to let go of the things that no longer make me happy.']
sad_affirmation = ['One bad moment doesn’t mean a bad day.', 'This feeling will not last forever.']
angry_affirmation = ['There is nothing wrong with feeling angry.', 'My anger does not always have to result in a strong reaction, but I am allowed to feel upset.', 'How I choose to express my anger is my responsibility.']
disgust_affirmation = ['Its okay to feel this way since everything is going to be alright.']
surprised_affirmation = ['How I express my emotions is my responsibility.', 'I am allowed to feel what I feel.', 'I am calm and content'] 

# Returns random affirmation based on emotion detected
# Neutral expression detected
if  emotion == ['happy']:
    print(random.choice(happy_affirmation))
# Happy expression detected 
elif emotion == ['surprised']:
    print(random.choice(surprised_affirmation))
# Sad expression detected
elif emotion == ['sad']:
    print(random.choice(sad_affirmation))
# Angry expression detected
elif emotion == ['angry']:
    print(random.choice(angry_affirmation))
# Disgust expression detected
elif emotion == ['disgust']:
    print(random.choice(disgust_affirmation))
# Surprise expression detected 
else:
    print(random.choice(neutral_affirmation)) 

    
