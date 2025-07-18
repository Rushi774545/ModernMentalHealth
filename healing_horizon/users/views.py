from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Question, Answer, AssessmentResult, ResponseOption , Expert
from .ml_model import predict_stress_level
from django.template.defaulttags import register
from django.shortcuts import render
import os
import json
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from elevenlabs.client import ElevenLabs
from django.http import JsonResponse

client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
def home(request):
    return render(request, 'users/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password. Please try again or register.')
            return redirect('login')
    
    return render(request, 'users/login.html')

@login_required
def dashboard(request):
    return render(request, 'users/dashboard.html', {'user': request.user})

@login_required
def start_assessment(request):
    questions = Question.objects.all().prefetch_related('options')
    
    if request.method == 'POST':
        answers = []
        for question in questions:
            answer_value = int(request.POST.get(f'q_{question.id}'))
            Answer.objects.create(
                question=question,
                user=request.user,
                value=answer_value
            )
            answers.append(answer_value)
        
        # Get prediction
        level, probabilities = predict_stress_level(answers)
        score = sum(answers) / (3 * len(answers)) * 100  # 3 is max value for options
        
        # Save result
        AssessmentResult.objects.create(
            user=request.user,
            score=score,
            level=level
        )
        
        return redirect('assessment_result')
    
    return render(request, 'users/assessment.html', {
        'questions': questions,
        'options_range': range(4)  # For template rendering
    })

@login_required
def assessment_result(request):
    result = AssessmentResult.objects.filter(user=request.user).latest('created_at')
    return render(request, 'users/assessment_result.html', {'result': result})


@login_required
def therapy_plan(request):
    day_images = {
        1: '3853149.jpg',
        2: '5184243.jpg',
        3: '5267933.jpg',
        4: '5272086.jpg',
        5: 'boho-8399739_1920.jpg',
        6: 'woman-8125244_1920.jpg',
        7: 'man-8707406_1920.png'
    }
    days = [
        {
            'day': 1,
            'title': 'Introduction to Mindfulness',
            'image': day_images[1],
            'techniques': [
                {'name': 'Meditation', 'duration': '10 mins', 'icon': 'fas fa-spa'},
                {'name': 'Self-Talk', 'duration': '5 mins', 'icon': 'fas fa-comment-dots'},
            ],
            'start_url': 'start_therapy_day', 
            'day_param': 1,
            'description': 'Start your journey with basic mindfulness exercises.'
        },
        {
            'day': 2,
            'title': 'Deep Breathing & Affirmations',
            'image': day_images[2],
            'techniques': [
                {'name': 'Meditation', 'duration': '15 mins', 'icon': 'fas fa-spa'},
                {'name': 'Self-Talk', 'duration': '10 mins', 'icon': 'fas fa-comment-dots'},
                {'name': 'Ho\'oponopono', 'duration': '7 mins', 'icon': 'fas fa-heart'},
            ],
            'start_url': 'start_therapy_day', 
            'day_param': 2,
            
            'description': 'Learn deep breathing techniques and positive affirmations.'
        },
        {
            'day': 3,
            'title': 'Body Scan & Self-Compassion',
            'image': day_images[3],
            'techniques': [
                {'name': 'Meditation', 'duration': '20 mins', 'icon': 'fas fa-spa'},
                {'name': 'Self-Talk', 'duration': '10 mins', 'icon': 'fas fa-comment-dots'},
            ],
            'start_url': 'start_therapy_day', 
            'day_param': 3,
            'description': 'Connect with your body and practice self-compassion.'
        },
        {
            'day': 4,
            'title': 'Loving-Kindness Meditation',
            'image': day_images[4],
            'techniques': [
                {'name': 'Meditation', 'duration': '15 mins', 'icon': 'fas fa-spa'},
                {'name': 'Self-Talk', 'duration': '10 mins', 'icon': 'fas fa-comment-dots'},
                {'name': 'Ho\'oponopono', 'duration': '10 mins', 'icon': 'fas fa-heart'},
            ],
            'start_url': 'start_therapy_day', 
            'day_param': 4,
            'description': 'Cultivate feelings of love and kindness towards yourself and others.'
        },
        {
            'day': 5,
            'title': 'Gratitude Practice',
            'image': day_images[5],
            'techniques': [
                 {'name': 'Meditation', 'duration': '20 mins', 'icon': 'fas fa-spa'},
                {'name': 'Self-Talk', 'duration': '15 mins', 'icon': 'fas fa-comment-dots'},
                {'name': 'Ho\'oponopono', 'duration': '10 mins', 'icon': 'fas fa-heart'},
            ],
            'start_url': 'start_therapy_day', 
            'day_param': 5,
            'description': 'Focus on gratitude and appreciation in your life.'
        },
        {
            'day': 6,
            'title': 'Stress Release Techniques',
            'image': day_images[6],
            'techniques': [
                {'name': 'Meditation', 'duration': '20 mins', 'icon': 'fas fa-spa'},
                {'name': 'Self-Talk', 'duration': '10 mins', 'icon': 'fas fa-comment-dots'},
            ],
            'start_url': 'start_therapy_day', 
            'day_param': 6,
            'description': 'Learn specific techniques to release stress and tension.'
        },
        {
            'day': 7,
            'title': 'Integration & Reflection',
            'image': day_images[7],
            'techniques': [
                {'name': 'Meditation', 'duration': '25 mins', 'icon': 'fas fa-spa'},
                {'name': 'Ho\'oponopono', 'duration': '15 mins', 'icon': 'fas fa-heart'},
                {'name': 'Self-Talk', 'duration': '10 mins', 'icon': 'fas fa-comment-dots'},
            ],
            'start_url': 'start_therapy_day', 
            'day_param': 7,
            'description': 'Reflect on your week and integrate what you\'ve learned.'
        }
    ]
    return render(request, 'users/therapy_plan.html', {'days': days})

@login_required
def start_therapy_day(request, day_number):
    # Duration in seconds for each day
    durations = {
        1: 5 * 60,   # 5 minutes
        2: 7 * 60,    # 7 minutes
        3: 10 * 60,   # 10 minutes
        4: 8 * 60,    # 8 minutes
        5: 6 * 60,    # 6 minutes
        6: 9 * 60,    # 9 minutes
        7: 12 * 60    # 12 minutes
    }
    
    context = {
        'day_number': day_number,
        'duration': durations.get(day_number, 5 * 60),
    }
    return render(request, 'users/therapy_session.html', context)

def voice_assistant(request):
    return render(request, 'users/voice_assistant.html')


@csrf_exempt
def assistant_chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '').lower()
        language = data.get('language', 'english')

        responses = {
            'english': {
        'greeting': "Hello! I'm your mental health assistant. How can I help you today?",
        'anxiety': "Do not worry belive in yourself ,For anxiety, try the 4-7-8 breathing technique: Inhale for 4 seconds, hold for 7 seconds, exhale for 8 seconds. Repeat 5 times. This helps calm your nervous system.",
        'depression': "Depression can feel overwhelming. Try these: 1) Take a 10-minute walk outside in sunlight, 2) Write down 3 things you're grateful for, 3) Reach out to a friend. Small steps matter.",
        'stress': "Do not worry When stressed, try the 5-4-3-2-1 grounding technique: Name 5 things you see, 4 things you can touch, 3 things you hear, 2 things you smell, and 1 thing you taste. This brings you back to the present moment.",
        'panic': "You are strong everything will be fine ,Just do the following: 1) Focus on your breathing, 2) Remind yourself this will pass, 3) Use cold water on your face to activate the dive reflex. Try box breathing: 4s inhale, 4s hold, 4s exhale.",
        'sleep': "Let me help you for better sleep: 1) Maintain a consistent sleep schedule, 2) Avoid screens 1 hour before bed, 3) Try a warm bath before bedtime, 4) Practice 10 minutes of mindfulness meditation.",
        'self_care': "Self-care is vital! Try these: 1) Take a digital detox for 1 hour daily, 2) Spend time in nature, 3) Practice saying no to protect your energy, 4) Keep a journal of your thoughts.",
        'motivation': "Don't forget that you are amazing you can do anything ,When you feel unmotivated: 1) Break tasks into 5-minute chunks, 2) Celebrate small wins, 3) Connect with your 'why' - what matters to you? 4) Try the 2-minute rule: just start for 2 minutes.",
        'relationships': "For relationship stress: 1) Practice active listening without judgment, 2) Use 'I feel' statements, 3) Set healthy boundaries, 4) Remember you can only control your own reactions.",
        'professional': "If you're considering professional help: Therapy can be incredibly beneficial. I recommend starting with cognitive behavioral therapy (CBT) which is effective for many concerns. Would you like help finding resources?",
        'crisis': "If you're in crisis: Please contact emergency services immediately. You can also reach the National Suicide Prevention Lifeline at 1-800-273-TALK (8255) or text HOME to 741741 for crisis support.",
        'default': "I'm here to listen. Could you tell me more about what you're experiencing? Understanding your feelings better helps me support you.",
        'grief': "Grief is a natural response to loss. Allow yourself to feel without judgment. Try these: 1) Create a small ritual to honor what you've lost, 2) Talk to someone who understands, 3) Write a letter expressing your feelings. Healing takes time.",
        'anger': "When feeling angry: 1) Take a pause and count to 10, 2) Use deep breathing to calm your body, 3) Express your feelings using 'I' statements when you're calmer, 4) Channel the energy into physical activity like walking or running.",
        'procrastination': "Every one procrastinate at some level you are not the only one ,to tackle procrastination: 1) Break tasks into tiny 2-minute steps, 2) Use the '5-second rule' - act immediately when you think of a task, 3) Eliminate distractions by turning off notifications, 4) Reward yourself after small completions.",
        'loneliness': "You are not lonely there are people around you who really care about you,For your loneliness: 1) Join community groups or online forums with shared interests, 2) Volunteer for causes you care about, 3) Practice self-compassion through positive self-talk, 4) Consider adopting a pet if circumstances allow.",
        'default': "I'm here to listen. Could you tell me more about what you're experiencing? Understanding your feelings better helps me support you."
    },
    'hindi': {
        'greeting': "नमस्ते! मैं आपकी मानसिक स्वास्थ्य सहायक हूँ। आप कैसा महसूस कर रहे हैं?",
        'anxiety': "चिंता मत करो अपने आप पर विश्वास रखो ,चिंता के लिए 4-7-8 साँस लेने की तकनीक आज़माएँ: 4 सेकंड साँस लें, 7 सेकंड रोकें, 8 सेकंड छोड़ें। 5 बार दोहराएँ। यह आपकी तंत्रिका तंत्र को शांत करने में मदद करता है।",
        'depression': "अवसाद भारी लग सकता है। ये आज़माएँ: 1) धूप में 10 मिनट टहलें, 2) 3 चीजें लिखें जिनके लिए आप आभारी हैं, 3) किसी मित्र से बात करें। छोटे कदम मायने रखते हैं।",
        'stress': "चिंता मत करो अपने आप पर विश्वास रखो ,तनाव होने पर 5-4-3-2-1 ग्राउंडिंग तकनीक आज़माएँ: 5 चीजें देखें, 4 चीजें छूएँ, 3 चीजें सुनें, 2 चीजें सूँघें, और 1 चीज चखें। यह आपको वर्तमान में वापस लाता है।",
        'panic': "आप मजबूत हैं, सब ठीक हो जाएगा, बस निम्नलिखित करें ,पैनिक अटैक के दौरान: 1) अपनी साँसों पर ध्यान दें, 2) खुद को याद दिलाएँ कि यह बीत जाएगा, 3) गोता रिफ्लेक्स को सक्रिय करने के लिए चेहरे पर ठंडा पानी डालें। बॉक्स ब्रीदिंग करें: 4s साँस लें, 4s रोकें, 4s छोड़ें।",
        'sleep': "मैं आपको बेहतर नींद के लिए मदद करूँगा: 1) नियमित सोने का समय रखें, 2) सोने से 1 घंटा पहले स्क्रीन से दूर रहें, 3) सोने से पहले गुनगुने पानी से नहाएँ, 4) 10 मिनट का माइंडफुलनेस मेडिटेशन करें।",
        'self_care': "आत्म-देखभाल ज़रूरी है! ये आज़माएँ: 1) रोज़ 1 घंटा डिजिटल डिटॉक्स करें, 2) प्रकृति में समय बिताएँ, 3) अपनी ऊर्जा बचाने के लिए 'ना' कहना सीखें, 4) अपने विचारों की डायरी रखें।",
        'motivation': "यह मत भूलिए कि आप अद्भुत हैं, आप कुछ भी कर सकते हैं, जब आप अप्रेरित महसूस करते हैं : 1) कामों को 5 मिनट के छोटे हिस्सों में बाँटें, 2) छोटी जीत का जश्न मनाएँ, 3) अपने 'क्यों' से जुड़ें - आपके लिए क्या महत्वपूर्ण है? 4) 2 मिनट नियम आज़माएँ: बस 2 मिनट के लिए शुरू करें।",
        'relationships': "रिश्तों के तनाव के लिए: 1) बिना न्याय किए सक्रिय सुनना सीखें, 2) 'मैं महसूस करता हूँ' वाक्यों का उपयोग करें, 3) स्वस्थ सीमाएँ निर्धारित करें, 4) याद रखें आप केवल अपनी प्रतिक्रियाओं को नियंत्रित कर सकते हैं।",
        'professional': "यदि आप पेशेवर मदद चाहते हैं: चिकित्सा बेहद फायदेमंद हो सकती है। मैं संज्ञानात्मक व्यवहार थेरेपी (CBT) शुरू करने की सलाह देता हूँ जो कई चिंताओं के लिए प्रभावी है। क्या आप संसाधन ढूंढने में मदद चाहेंगे?",
        'crisis': "यदि आप संकट में हैं: कृपया तुरंत आपातकालीन सेवाओं से संपर्क करें। आप राष्ट्रीय आत्महत्या रोकथाम लाइफलाइन 1-800-273-8255 पर भी कॉल कर सकते हैं या संकट सहायता के लिए 741741 पर HOME टेक्स्ट कर सकते हैं।",
        'default': "मैं सुनने के लिए यहाँ हूँ। क्या आप अपनी भावनाओं के बारे में और बता सकते हैं? आपकी भावनाओं को बेहतर समझने से मुझे आपकी सहायता करने में मदद मिलेगी।",
        'grief': "दुःख खोने की एक स्वाभाविक प्रतिक्रिया है। खुद को बिना न्याय किए महसूस करने दें। ये आज़माएँ: 1) जो खो गया है उसका सम्मान करने के लिए एक छोटा सा रस्म बनाएँ, 2) किसी समझदार व्यक्ति से बात करें, 3) अपनी भावनाओं को व्यक्त करते हुए एक पत्र लिखें। घाव भरने में समय लगता है।",
        'anger': "गुस्सा आने पर: 1) रुकें और 10 तक गिनें, 2) गहरी साँस लेकर शरीर को शांत करें, 3) शांत होने पर 'मैं' वाक्यों से अपनी भावनाएँ बताएँ, 4) टहलने या दौड़ने जैसी शारीरिक गतिविधि में उर्जा लगाएँ।",
        'procrastination': "हर कोई किसी न किसी स्तर पर टालमटोल करता है, आप अकेले नहीं हैं ,टालमटोल से निपटने के लिए: 1) कामों को 2 मिनट के छोटे चरणों में बाँटें, 2) '5-सेकंड नियम' अपनाएँ - काम का ख्याल आते ही तुरंत करें, 3) सूचनाएँ बंद करके ध्यान भटकाने वाली चीजें हटाएँ, 4) छोटे पूरा होने पर खुद को पुरस्कृत करें।",
        'loneliness': "आप अकेले नहीं हैं, आपके आस-पास ऐसे लोग हैं जो सचमुच आपकी परवाह करते हैं ,अकेलापन महसूस होने पर: 1) सामुदायिक समूहों या रुचि वाले ऑनलाइन मंचों में शामिल हों, 2) अपनी पसंद के सामाजिक कार्यों में स्वेच्छा से भाग लें, 3) स्वयं से दयालु बातें करके आत्म-करुणा का अभ्यास करें, 4) परिस्थिति अनुकूल हो तो पालतू जानवर अपनाने पर विचार करें।",
        'default': "मैं सुनने के लिए यहाँ हूँ। क्या आप अपनी भावनाओं के बारे में और बता सकते हैं? आपकी भावनाओं को बेहतर समझने से मुझे आपकी सहायता करने में मदद मिलेगी।"
    }

    
 }

# Detect intent with more keywords
        response_key = 'default'
        user_message = user_message.lower()
        if any(word in user_message for word in ['hello', 'hi', 'hey', 'namaste', 'namaskar']):
            response_key = 'greeting'
        elif any(word in user_message for word in ['suicide', 'end it all', 'kill myself', 'marne', 'khatam', 'aatmahatya', 'जान दे दूंगा']):
            response_key = 'crisis'
        elif any(word in user_message for word in ['anxious', 'anxiety', 'nervous', 'ghabrana', 'chinta', 'ghabrahat', 'घबराहट', 'बेचैनी']):
            response_key = 'anxiety'
        elif any(word in user_message for word in ['depress', 'sad', 'hopeless', 'udas', 'nirash', 'bechain', 'उदासी', 'निराशा']):
            response_key = 'depression'
        elif any(word in user_message for word in ['grief', 'loss', 'mourn', 'dukh', 'shok', 'नुकसान', 'शोक', 'वियोग']):
            response_key = 'grief'
        elif any(word in user_message for word in ['angry', 'anger', 'furious', 'gussa', 'krodh', 'naraz', 'गुस्सा', 'क्रोध', 'चिढ़']):
            response_key = 'anger'
        elif any(word in user_message for word in ['stress', 'overwhelm', 'pressure', 'tanaav', 'bhoj', 'dabav', 'तनाव', 'दबाव']):
            response_key = 'stress'
        elif any(word in user_message for word in ['panic', 'attack', 'darr', 'sankat', 'heart race', 'dil dhadakna', 'दौरा', 'सनक']):
            response_key = 'panic'
        elif any(word in user_message for word in ['sleep', 'insomnia', 'sone', 'neend', 'nind na aana', 'नींद', 'अनिद्रा']):
            response_key = 'sleep'
        elif any(word in user_message for word in ['self care', 'self-care', 'khud ka khayal', 'apna dhyan', 'aatm-sambhaal', 'आत्म देखभाल']):
            response_key = 'self_care'
        elif any(word in user_message for word in ['procrastinate', 'delay', 'kal kare', 'talna', 'टालना', 'स्थगित']):
            response_key = 'procrastination'
        elif any(word in user_message for word in ['lonely', 'alone', 'akela', 'tanha', 'अकेला', 'एकांत']):
            response_key = 'loneliness'
        elif any(word in user_message for word in ['motivate', 'lazy', 'unmotivated', 'utsahit', 'josh', 'himmat', 'प्रेरणा', 'उत्साह']):
            response_key = 'motivation'
        elif any(word in user_message for word in ['relationship', 'partner', 'wife', 'husband', 'friend', 'rishta', 'sambandh', 'pati', 'patni', 'रिश्ता', 'संबंध']):
            response_key = 'relationships'
        elif any(word in user_message for word in ['therapist', 'counselor', 'doctor', 'professional', 'therapy', 'chikitsak', 'mansik', 'upchaarak', 'चिकित्सक', 'पेशेवर']):
            response_key = 'professional'


        
        # Simple response logic - you can expand this with more sophisticated NLP
      
        
        # Get appropriate response
        lang_responses = responses.get(language, responses['english'])
        response = lang_responses.get(response_key, lang_responses['default'])
        
        return JsonResponse({'response': response})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def generate_speech(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            text = data.get('text', '')
            language = data.get('language', 'english')
            
            if not text:
                return JsonResponse({'error': 'No text provided'}, status=400)
            
            # Voice selection
            voice = "Alexandra" if language == "english" else "Kanika"
            
            # Generate audio using the client
            audio = client.generate(
                text=text,
                voice=voice,
                model="eleven_multilingual_v2"  # Updated model
            )
            
            # Ensure media directory exists
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
            
            # Save audio
            audio_path = os.path.join(settings.MEDIA_ROOT, 'response.mp3')
            with open(audio_path, 'wb') as f:
                f.write(audio)
            
            return JsonResponse({'audio_url': f"{settings.MEDIA_URL}response.mp3"})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
def expert_list(request):
    location = request.GET.get('location', '')
    expert_type = request.GET.get('type', '')
    
    experts = Expert.objects.all()
    
    if location:
        experts = experts.filter(location__icontains=location)
    if expert_type:
        experts = experts.filter(expert_type=expert_type)
    
    context = {
        'experts': experts,
        'location': location,
        'selected_type': expert_type
    }
    return render(request, 'users/expert_list.html', context)


def expert_signin(request):
    return render(request, 'users/expert_signin.html')