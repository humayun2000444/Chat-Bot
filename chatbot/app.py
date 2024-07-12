from flask import Flask, render_template, request, jsonify
import mysql.connector
import nltk
from nltk.chat.util import Chat, reflections

app = Flask(__name__)

# Configure MySQL connection with new user credentials
db = mysql.connector.connect(
    host="localhost",
    user="humayun",
    password="Takay1takaane$",
    database="chatbot_logs"
)

pairs = [
    (r'hi|hello|hey',
     ['Hello!', 'Hey there!', 'Hi!']),
    (r'help',
     ['Sure, how can I assist you?', 'What do you need help with?']),
    (r'bye|goodbye',
     ['Goodbye!', 'Have a great day!', 'Bye.']),
    (r'what is good mental health\??',
     ['Good mental health is feeling good about yourself, others, and your environment.']),
    (r'half of all mental health disorders begin before what age\??',
     ['Half of all mental health disorders begin before the age of 14.']),
    (r'true or false\? you can "work" on your mental health\.',
     ['True! Good mental health is something you build with daily exercises and good lifestyle habits.']),
    (r'how can you improve your mental health\??',
     ['You can improve your mental health by spending time with friends and family.']),
    (r'when you\'re feeling stressed or anxious, what\'s the best way to ease the pressure\??',
     ['Meditation is the best way to ease the pressure when you are feeling stressed or anxious.']),
    (r'what clues might alert you that a friend or classmate is in distress\??',
     ['Signs like getting angry over nothing, always seeming sad, or not wanting to take part in activities may indicate that a friend or classmate is in distress.']),
    (r'when you\'re fighting with a friend, what\'s the best way to act\??',
     ['Take a break to calm down before responding.']),
    (r'if a friend or classmate is showing signs of distress, where can you find resources to help\??',
     ['You can find resources at school by talking to a Special Education Technician (SET), or outside school by contacting Tel-Jeunes or speaking with parents, family, or a trustworthy adult.']),
    (r'true or false\? when you don’t feel well, the best course of action is to wait it out\.',
     ['False! When you’re feeling down, it’s important to confide in someone you trust and who can direct you to the right resources if needed.']),
    (r'what is a parasitic thought\??',
     ['A parasitic thought is a thought that causes you to suffer and prevents you from moving forward.']),
    (r'what should you do when you feel stressed\??',
     ['You should sort out your thoughts and meditate, and talk to yourself the way you’d talk to a friend.']),
    (r'what is self-compassion\??',
     ['Self-compassion is practicing positive self-talk, talking to yourself with kindness and compassion.']),
    (r'true or false\? good mental health means not having a mental illness\.',
     ['False. Good mental health means feeling good about yourself, others, and your environment.']),
    (r'what are the main aspects of mental health\??',
     ['Mental health is a state of emotional and mental well-being related to oneself, others, and different environments.']),
    (r'what is a good way to maintain mental health\??',
     ['Maintaining mental health includes sleeping 8-10 hours a night, eating healthily, exercising daily, and managing screen time.']),
    (r'why is it important to take care of mental health at a young age\??',
     ['It is important because half of all mental health disorders begin before the age of 14 and 75% before the age of 22.']),
    (r'how can meditation help with stress\??',
     ['Meditation helps by allowing you to take a break from your thoughts and focus on the present moment.']),
    (r'what should you do when fighting with a friend\??',
     ['Take a break to calm down before responding.']),
    (r'what resources are available for mental health support\??',
     ['Resources include talking to a Special Education Technician at school, contacting Tel-Jeunes, or speaking with a trustworthy adult.']),
    (r'what is useful thinking\??',
     ['Useful thinking is based on your senses, takes place in the present moment, and offers possible solutions.']),
    (r'how can self-compassion help\??',
     ['Self-compassion involves talking to yourself with kindness and compassion, helping to actively relieve your suffering.']),

     (r'হাই|হ্যালো|হেই',
    ['হ্যালো!', 'আরে আছে!', 'হাই!']),
    (r'আর|সাহায্য',
     ['অবশ্যই, আমি কীভাবে আপনাকে সাহায্য করতে পারি?', 'আপনার কী সাহায্যের প্রয়োজন?']),
    ('আর|বিদায়|বিদায়',
     ['বিদায়!', 'দিনটি ভালো কাটুক!', 'বিদায়']),
    (r'ভাল মানসিক স্বাস্থ্য কি\??',
     ['ভাল মানসিক স্বাস্থ্য আপনার, অন্যদের এবং আপনার পরিবেশ সম্পর্কে ভাল অনুভব করে।']),
    (r'সমস্ত মানসিক স্বাস্থ্য ব্যাধির অর্ধেক শুরু হয় কত বয়সের আগে\??',
     ['সমস্ত মানসিক স্বাস্থ্য ব্যাধির অর্ধেক 14 বছর বয়সের আগে শুরু হয়।']),
    (r'সত্য না মিথ্যা\? আপনি আপনার মানসিক স্বাস্থ্যের উপর "কাজ" করতে পারেন।',
     ['সত্যি! ভাল মানসিক স্বাস্থ্য এমন একটি জিনিস যা আপনি প্রতিদিনের ব্যায়াম এবং ভাল জীবনযাত্রার অভ্যাস দিয়ে তৈরি করেন।']),
    (r'কিভাবে আপনি আপনার মানসিক স্বাস্থ্যের উন্নতি করতে পারেন\??',
     ['বন্ধু ও পরিবারের সাথে সময় কাটানোর মাধ্যমে আপনি আপনার মানসিক স্বাস্থ্যের উন্নতি করতে পারেন।']),
    (r'যখন আপনি চাপ বা উদ্বিগ্ন বোধ করেন, চাপ কমানোর সর্বোত্তম উপায় কী\??',
     ['যখন আপনি চাপ বা উদ্বিগ্ন বোধ করেন তখন চাপ কমানোর সর্বোত্তম উপায় হল ধ্যান।']),
    (r'কোন ক্লুস আপনাকে সতর্ক করতে পারে যে একজন বন্ধু বা সহপাঠী বিপদে আছে\??',
     ['কোন কিছুর জন্য রাগ করা, সর্বদা দু: খিত মনে হওয়া, বা ক্রিয়াকলাপে অংশ নিতে না চাওয়ার মতো লক্ষণগুলি বোঝাতে পারে যে কোনও বন্ধু বা সহপাঠী কষ্টে রয়েছে।']),
    (r'যখন আপনি কোনো বন্ধুর সাথে ঝগড়া করছেন, তখন অভিনয় করার সবচেয়ে ভালো উপায় কী?',
     ['প্রতিক্রিয়া করার আগে শান্ত হওয়ার জন্য বিরতি নিন।']),
    (r'যদি কোনো বন্ধু বা সহপাঠী কষ্টের লক্ষণ দেখায়, তাহলে আপনি সাহায্য করার জন্য সংস্থান কোথায় পাবেন\??',
     ['আপনি একটি স্পেশাল এডুকেশন টেকনিশিয়ানের (SET) সাথে কথা বলে বা স্কুলের বাইরে Tel-Jeunes-এ যোগাযোগ করে বা পিতামাতা, পরিবার বা বিশ্বস্ত প্রাপ্তবয়স্কদের সাথে কথা বলে সম্পদ খুঁজে পেতে পারেন।']),
    (r'সত্য না মিথ্যা\? যখন আপনি ভাল অনুভব করেন না, তখন সর্বোত্তম পদক্ষেপ হল অপেক্ষা করা।',
     ['মিথ্যা! আপনি যখন মন খারাপ করেন, তখন আপনি বিশ্বাস করেন এমন কাউকে বিশ্বাস করা গুরুত্বপূর্ণ এবং প্রয়োজনে যিনি আপনাকে সঠিক সংস্থানগুলির দিকে পরিচালিত করতে পারেন।']),
    (r'একটি পরজীবী চিন্তা কি?',
     ['একটি পরজীবী চিন্তা এমন একটি চিন্তা যা আপনাকে কষ্ট দেয় এবং আপনাকে এগিয়ে যেতে বাধা দেয়।']),
    (r'আপনি যখন চাপ অনুভব করেন তখন আপনার কী করা উচিত\??',
     ['আপনি আপনার চিন্তাভাবনাগুলি সাজান এবং ধ্যান করুন এবং নিজের সাথে কথা বলুন যেভাবে আপনি একজন বন্ধুর সাথে কথা বলেন।']),
    (r'আত্ম-সহানুভূতি কি\??',
     ['আত্ম-সহানুভূতি হল ইতিবাচক স্ব-কথোপকথন অনুশীলন করা, দয়া এবং সহানুভূতির সাথে নিজের সাথে কথা বলা।']),
    (r'সত্য না মিথ্যা\? ভালো মানসিক স্বাস্থ্য মানে মানসিক অসুস্থতা না হওয়া\।',
     ['মিথ্যা। ভাল মানসিক স্বাস্থ্য মানে নিজেকে, অন্যদের এবং আপনার পরিবেশ সম্পর্কে ভাল বোধ করা।']),
    (r'মানসিক স্বাস্থ্যের প্রধান দিকগুলো কি ?',
     ['মানসিক স্বাস্থ্য হল নিজের, অন্যদের এবং বিভিন্ন পরিবেশের সাথে সম্পর্কিত মানসিক এবং মানসিক সুস্থতার একটি অবস্থা।']),
    (r'মানসিক স্বাস্থ্য বজায় রাখার একটি ভাল উপায়\??',
     ['মানসিক স্বাস্থ্য বজায় রাখার মধ্যে রয়েছে রাতে 8-10 ঘন্টা ঘুমানো, স্বাস্থ্যকর খাবার খাওয়া, প্রতিদিন ব্যায়াম করা এবং স্ক্রিন টাইম পরিচালনা করা।']),
    (r'কেন অল্প বয়সে মানসিক স্বাস্থ্যের যত্ন নেওয়া জরুরী\??',
     ['এটি গুরুত্বপূর্ণ কারণ সমস্ত মানসিক স্বাস্থ্য ব্যাধির অর্ধেক শুরু হয় 14 বছর বয়সের আগে এবং 75�22 বছর বয়সের আগে।']),
    (r'কীভাবে ধ্যান মানসিক চাপে সাহায্য করতে পারে\??',
     ['ধ্যান আপনাকে আপনার চিন্তাভাবনা থেকে বিরতি নিতে এবং বর্তমান মুহুর্তে ফোকাস করার অনুমতি দিয়ে সাহায্য করে।']),
    (r'বন্ধুর সাথে ঝগড়া করার সময় আপনার কি করা উচিত\??',
     ['প্রতিক্রিয়া করার আগে শান্ত হওয়ার জন্য বিরতি নিন।']),
    (r'মানসিক স্বাস্থ্য সহায়তার জন্য কি কি সম্পদ উপলব্ধ\??',
     ['সম্পদগুলির মধ্যে রয়েছে স্কুলে একজন বিশেষ শিক্ষা টেকনিশিয়ানের সাথে কথা বলা, টেল-জিউনসের সাথে যোগাযোগ করা, বা একজন বিশ্বস্ত প্রাপ্তবয়স্কের সাথে কথা বলা।']),
    (r'উপযোগী চিন্তা কি\??',
     ['উপযোগী চিন্তা আপনার ইন্দ্রিয়ের উপর ভিত্তি করে, বর্তমান মুহুর্তে সঞ্চালিত হয়, এবং সম্ভাব্য সমাধান প্রস্তাব করে।']),
    (r'আত্ম-সহানুভূতি কীভাবে সাহায্য করতে পারে\??',
     ['আত্ম-সহানুভূতির মধ্যে রয়েছে দয়া এবং সহানুভূতির সাথে নিজের সাথে কথা বলা, সক্রিয়ভাবে আপনার দুঃখকষ্ট দূর করতে সহায়তা করা।'])
]

@app.route('/')
def index():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM chat_logs")
    logs = cursor.fetchall()
    cursor.close()
    return render_template('index.html', chat_logs=logs)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    chat = Chat(pairs, reflections)
    response = chat.respond(user_input)
    
    # Save chat log to MySQL
    save_chat_log('user_id_here', user_input, response)
    
    return jsonify({'message': response})

def save_chat_log(user_id, user_message, bot_response):
    cursor = db.cursor()
    insert_query = "INSERT INTO chat_logs (user_id, message, bot_response) VALUES (%s, %s, %s);"
    cursor.execute(insert_query, (user_id, user_message, bot_response))
    db.commit()
    cursor.close()

if __name__ == '__main__':
    nltk.download('punkt')  # Ensure punkt tokenizer data is downloaded
    app.run(debug=True)
