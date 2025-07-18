from django.core.management.base import BaseCommand
from users.models import Question, ResponseOption

QUESTIONS = [
    {
        'text': "Little interest or pleasure in doing things",
        'category': "Depression",
        'options': [
            {"text": "Not at all", "value": 0},
            {"text": "Several days", "value": 1},
            {"text": "More than half the days", "value": 2},
            {"text": "Nearly every day", "value": 3}
        ]
    },
    {
        'text': "Feeling down, depressed, or hopeless",
        'category': "Depression",
        'options': [
            {"text": "Not at all", "value": 0},
            {"text": "Several days", "value": 1},
            {"text": "More than half the days", "value": 2},
            {"text": "Nearly every day", "value": 3}
        ]
    },
    {
        'text': "Trouble falling or staying asleep, or sleeping too much",
        'category': "Depression",
        'options': [
            {"text": "Not at all", "value": 0},
            {"text": "Several days", "value": 1},
            {"text": "More than half the days", "value": 2},
            {"text": "Nearly every day", "value": 3}
        ]
    },
    {
        'text': "Feeling tired or having little energy",
        'category': "Depression",
        'options': [
            {"text": "Not at all", "value": 0},
            {"text": "Several days", "value": 1},
            {"text": "More than half the days", "value": 2},
            {"text": "Nearly every day", "value": 3}
        ]
    },
    {
        'text': "Poor appetite or overeating",
        'category': "Depression",
        'options': [
            {"text": "Not at all", "value": 0},
            {"text": "Several days", "value": 1},
            {"text": "More than half the days", "value": 2},
            {"text": "Nearly every day", "value": 3}
        ]
    },
    {
        'text': "Feeling bad about yourself - or that you're a failure or have let yourself or your family down",
        'category': "Depression",
        'options': [
            {"text": "Not at all", "value": 0},
            {"text": "Several days", "value": 1},
            {"text": "More than half the days", "value": 2},
            {"text": "Nearly every day", "value": 3}
        ]
    },
    {
        'text': "Trouble concentrating on things, such as reading the newspaper or watching television",
        'category': "Depression",
        'options': [
            {"text": "Not at all", "value": 0},
            {"text": "Several days", "value": 1},
            {"text": "More than half the days", "value": 2},
            {"text": "Nearly every day", "value": 3}
        ]
    },
    {
        'text': "Moving or speaking so slowly that other people could have noticed. Or the opposite - being so fidgety or restless that you have been moving around a lot more than usual",
        'category': "Depression",
        'options': [
            {"text": "Not at all", "value": 0},
            {"text": "Several days", "value": 1},
            {"text": "More than half the days", "value": 2},
            {"text": "Nearly every day", "value": 3}
        ]
    },
    {
        'text': "Thoughts that you would be better off dead or of hurting yourself in some way",
        'category': "Depression",
        'options': [
            {"text": "Not at all", "value": 0},
            {"text": "Several days", "value": 1},
            {"text": "More than half the days", "value": 2},
            {"text": "Nearly every day", "value": 3}
        ]
    },
    {
        'text': "Feeling nervous, anxious, or on edge",
        'category': "Anxiety",
        'options': [
            {"text": "Not at all", "value": 0},
            {"text": "Several days", "value": 1},
            {"text": "More than half the days", "value": 2},
            {"text": "Nearly every day", "value": 3}
        ]
    },
    {
        'text': "Not being able to stop or control worrying",
        'category': "Anxiety",
        'options': [
            {"text": "Not at all", "value": 0},
            {"text": "Several days", "value": 1},
            {"text": "More than half the days", "value": 2},
            {"text": "Nearly every day", "value": 3}
        ]
    },
    {
        'text': "Worrying too much about different things",
        'category': "Anxiety",
        'options': [
            {"text": "Not at all", "value": 0},
            {"text": "Several days", "value": 1},
            {"text": "More than half the days", "value": 2},
            {"text": "Nearly every day", "value": 3}
        ]
    },
    {
        'text': "Trouble relaxing",
        'category': "Anxiety",
        'options': [
            {"text": "Not at all", "value": 0},
            {"text": "Several days", "value": 1},
            {"text": "More than half the days", "value": 2},
            {"text": "Nearly every day", "value": 3}
        ]
    },
    {
        'text': "Being so restless that it's hard to sit still",
        'category': "Anxiety",
        'options': [
            {"text": "Not at all", "value": 0},
            {"text": "Several days", "value": 1},
            {"text": "More than half the days", "value": 2},
            {"text": "Nearly every day", "value": 3}
        ]
    },
    {
        'text': "Becoming easily annoyed or irritable",
        'category': "Anxiety",
        'options': [
            {"text": "Not at all", "value": 0},
            {"text": "Several days", "value": 1},
            {"text": "More than half the days", "value": 2},
            {"text": "Nearly every day", "value": 3}
        ]
    },
    {
        'text': "Feeling afraid as if something awful might happen",
        'category': "Anxiety",
        'options': [
            {"text": "Not at all", "value": 0},
            {"text": "Several days", "value": 1},
            {"text": "More than half the days", "value": 2},
            {"text": "Nearly every day", "value": 3}
        ]
    },
    {
        'text': "Feeling tense or having muscle tension",
        'category': "Stress",
        'options': [
            {"text": "Not at all", "value": 0},
            {"text": "Several days", "value": 1},
            {"text": "More than half the days", "value": 2},
            {"text": "Nearly every day", "value": 3}
        ]
    },
    {
        'text': "Difficulty controlling your temper",
        'category': "Stress",
        'options': [
            {"text": "Not at all", "value": 0},
            {"text": "Several days", "value": 1},
            {"text": "More than half the days", "value": 2},
            {"text": "Nearly every day", "value": 3}
        ]
    },
    {
        'text': "Avoiding situations that make you anxious",
        'category': "Stress",
        'options': [
            {"text": "Not at all", "value": 0},
            {"text": "Several days", "value": 1},
            {"text": "More than half the days", "value": 2},
            {"text": "Nearly every day", "value": 3}
        ]
    },
    {
        'text': "Experiencing sudden episodes of intense fear or discomfort",
        'category': "Stress",
        'options': [
            {"text": "Not at all", "value": 0},
            {"text": "Several days", "value": 1},
            {"text": "More than half the days", "value": 2},
            {"text": "Nearly every day", "value": 3}
        ]
    },
    {
        'text': "Feeling disconnected from yourself or your surroundings",
        'category': "Dissociation",
        'options': [
            {"text": "Not at all", "value": 0},
            {"text": "Several days", "value": 1},
            {"text": "More than half the days", "value": 2},
            {"text": "Nearly every day", "value": 3}
        ]
    },
    {
        'text': "Persistent unpleasant thoughts or images",
        'category': "OCD",
        'options': [
            {"text": "Not at all", "value": 0},
            {"text": "Several days", "value": 1},
            {"text": "More than half the days", "value": 2},
            {"text": "Nearly every day", "value": 3}
        ]
    }
]

class Command(BaseCommand):
    help = 'Loads assessment questions with response options into database'

    def handle(self, *args, **options):
        Question.objects.all().delete()  # Clear existing questions
        
        for i, q_data in enumerate(QUESTIONS, start=1):
            question = Question.objects.create(
                text=q_data['text'],
                category=q_data.get('category', ''),
                weight=1.0 + (i * 0.02),
                display_order=i
            )
            
            for j, option in enumerate(q_data['options'], start=1):
                ResponseOption.objects.create(
                    question=question,
                    text=option['text'],
                    value=option['value'],
                    display_order=j
                )
            
            self.stdout.write(f"Loaded question {i}: {q_data['text'][:50]}... with {len(q_data['options'])} options")
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully loaded {len(QUESTIONS)} questions with response options'
        ))