from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
# values from docker file from docker compose from .env
proxy_port = os.environ.get('FLASK_APP_PROXY')
host_ip = os.environ.get('FLASK_APP_HOST_IP')
host_name = os.environ.get('FLASK_APP_HOST_NAME')

if os.environ.get("FLASK_APP_PROD") == "false" or os.environ.get("FLASK_APP_PROD") == None:
    debug = True
    allowed_origins = [f"http://localhost:{proxy_port}", 
    f"https://localhost:{proxy_port}", f"http://{host_name}:{proxy_port}", 
    f"https://{host_name}:{proxy_port}",f"http://{host_ip}:{proxy_port}", 
    f"https://{host_ip}:{proxy_port}", "https://localhost:643", "http://localhost:3000"]
else:
    debug = False
    allowed_origins = [f"http://{host_name}:{proxy_port}", f"https://{host_name}:{proxy_port}",
    f"http://{host_ip}:{proxy_port}", f"https://{host_ip}:{proxy_port}",]
app.config["DEBUG"] = debug


CORS(app, resources={r"/*": {"origins": allowed_origins}})


surveys = {
    "riskassessment": {
        "description": 
'''
# Financial Risk Assessment
Whether it be Netflix, Apple Music or Domino&apos;s Pizza,
personalizaiton requires user preferences. Without an understanding of
the factors that contribute to a users taste, a recommendation system
can never know what is the appropriate next offer.

Learning user preferences in financial services, appears to be
behavior observation, experiment and survey research combined in a
statistically significant manner. When utilizing methods that have
proven significance, repeatable and increasingly accurate assumtions
can be made upon user preferences from the factors we know correlate
with our customer base.

From discussions as well as research into how others in the financial
services are capturing user preferences, it appears as if there is an
opportunity to offer a better service.

Where others in the industry are viewing customer inteake as an after
thought - if we view it as the first touchpoint in a personalizaiton
pipeline, we can build onboarding into insights that greatly benefit
both the advisor and their customer.

## The Big Five Personality Traits
Research has shown that personality factors can provide statistically
significant insight into the preferences of wealth customers.

It has been shown that the Big Five Personality trait metrics
&quot;significantly predict financial risk tolerance,&quot; and thus
can begin to model user prefernce for investment instruments. The
applications possible from this base are many:

## Instructions

Describe yourself as you generally are now, not as you wish to be in
the future.

Describe yourself as you honestly see yourself, in relation to other
people you know of the same sex as you are, and roughly your same age.

Indicate for each statement below how much the statement describes
you:
''',
        "traits": ["extraversion", "imagination", "neuroticism", "conscientiousness", "agreeableness"],
        "sentiments": ["positive", "negative"],
        "css": {
            "matrix": {
                "root": "table table-striped",
            },
        },
        "questions": [ 
            {
                "type": "dropdown",
                "name": "gender",
                "title": "Select your gender",
                "isRequired": True,
                "choices": [
                    {"value": "male", "text": "Male"}, 
                    {"value": "female", "text": "Female"},
                    {"value": "other", "text": "Other"},
                    ],
                "valueName": "gender",
            },
            {
                "type": "dropdown",
                "name": "education",
                "title": "Select your education level",
                "isRequired": True,
                "valueName": "education",
                "choices": [
                    {"value": "low", "text":"Low (below highscool)"},
                    {"value": "medium", "text": "Medium (highschool+equivalent)"},
                    {"value": "high", "text": "High (above highschool)"},
                ],
            },
            {
                "type": "text",
                "name": "age",
                "title": "Enter your age",
                "inputType": "number",
                "isRequired": True,
            },
            {
                "type": "text",
                "name": "income",
                "title": "Enter your gross total income",
                "inputType": "number",
                "isRequired": True,
                # this has to be divided by 100,000
            },
            {
                "type": "matrix",
                "name": "financeKnowledge",
                "title": "How knowledgable are you in finance?",        
        "columns": [
                    { "value": 1, "text": "Not Knowledgable" },
                    { "value": 2, "text": "Somewhat Knowledgable" },
                    { "value": 3, "text": "Knowledgable" },
                    { "value": 4, "text": "Very Knowledgable" },
                ],
                "rows": [
                    {
                    "value": "financeKnowledge",
                    "text": "Finance Knowledge",
                    },
                ],
                "isRequired": True,
            },
            {
                "type": "boolean",
                "name": "financeAdministrator",
                "label": "Are you the financial administrator of your household?",
                "isRequired": True,
            },
            {
                "type": "boolean",
                "name": "householdHead",
                "label": "Are you the head of your household?",
                "isRequired": True,
            },
            {
                "type": "boolean",
                "name": "spouse",
                "label": "Do you have a spouse (married) or permanment partner?",
                "isRequired": True,
            },
            {
                "type": "boolean",
                "name": "mainWageEarner",
                "label": "Are you the main wage earner in your household?",
                "isRequired": True,
            },
            {
                "type": "matrix",
                "name": "personality",
                "title": "IPIP Big-Five Personality Traits Test. Indicate for each statement below how much the statement describes you",
                "columns": [
                    { "value": 1, "text": "Very Inaccurate" },
                    { "value": 2, "text": "Moderately Inacurate" },
                    { "value": 3, "text": "Neither Accurate nor Inaccurate)," },
                    { "value": 4, "text": "Moderately Accurate" },
                    { "value": 5, "text": "Very Accurate" },
                ],
                "rows": [
                    {
                        "value": "I am the life of the party",
                        "text": "I am the life of the party",
                        "trait": "extraversion",
                        "sentiment": "positive", 
                    },
                    {
                        "value": "I feel little concern for others",
                        "text": "I feel little concern for others",
                        "trait": "agreeableness",
                        "sentiment": "negative", 
                    },
                    {
                        "value": "I am always prepared",
                        "text": "I am always prepared",
                        "trait": "conscientiousness",
                        "sentiment": "positive", 
                    },
                    {
                        "value": "I get stressed out easily",
                        "text": "I get stressed out easily",
                        "trait": "neuroticism",
                        "sentiment": "negative", 
                    },
                    {
                        "value": "I have a rich vocabularly",
                        "text": "I have a rich vocabularly",
                        "trait": "imagination",
                        "sentiment": "positive", 
                    },
                    { 
                        "value": "I don't talk a lot",
                        "text": "I don't talk a lot",
                        "trait": "extraversion",
                        "sentiment": "negative", 
                    },
                    {
                        "value": "I am interested in people",
                        "text": "I am interested in people",
                        "trait": "agreeableness",
                        "sentiment": "positive", 
                    },
                    {
                        "value": "I leave my belongings around",
                        "text": "I leave my belongings around",
                        "trait": "conscientiousness",
                        "sentiment": "negative", 
                    },
                    {
                        "value": "I am relaxed most of the time",
                        "text": "I am relaxed most of the time",
                        "trait": "neuroticism",
                        "sentiment": "positive", 
                    },
                    {
                        "value": "I have difficulty understanding abstract ideas",
                        "text": "I have difficulty understanding abstract ideas",
                        "trait": "imagination",
                        "sentiment": "negative", 
                    },
                            { 
                        "value": "I feel comfortable around people",
                        "text": "I feel comfortable around people",
                        "trait": "extraversion",
                        "sentiment": "positive", 
                    },
                    {
                        "value": "I insult people",
                        "text": "I insult people",
                        "trait": "agreeableness",
                        "sentiment": "negative", 
                    },
                    {
                        "value": "I pay attention to details",
                        "text": "I pay attention to details",
                        "trait": "conscientiousness",
                        "sentiment": "positive", 
                    },
                    {
                        "value": "I worry about things",
                        "text": "I worry about things",
                        "trait": "neuroticism",
                        "sentiment": "negative", 
                    },
                    {
                        "value": "I have a vivid imagination",
                        "text": "I have a vivid imagination",
                        "trait": "imagination",
                        "sentiment": "positive", 
                    },
                    { 
                        "value": "I keep in the background",
                        "text": "I keep in the background",
                        "trait": "extraversion",
                        "sentiment": "negative", 
                    },
                    {
                        "value": "I symathize with others feelings",
                        "text": "I symathize with others feelings",
                        "trait": "agreeableness",
                        "sentiment": "positive", 
                    },
                    {
                        "value": "I make a mess of things",
                        "text": "I make a mess of things",
                        "trait": "conscientiousness",
                        "sentiment": "negative", 
                    },
                    {
                        "value": "I seldom feel blue",
                        "text": "I seldom feel blue",
                        "trait": "neuroticism",
                        "sentiment": "positive", 
                    },
                    {
                        "value": "I am not interested in abstract ideas",
                        "text": "I am not interested in abstract ideas",
                        "trait": "imagination",
                        "sentiment": "negative", 
                    },
                    { 
                        "value": "I start conversations",
                        "text": "I start conversations",
                        "trait": "extraversion",
                        "sentiment": "positive", 
                    },
                    {
                        "value": "I am not interested in other people's problems",
                        "text": "I am not interested in other people's problems",
                        "trait": "agreeableness",
                        "sentiment": "negative", 
                    },
                    {
                        "value": "I get chores done right away",
                        "text": "I get chores done right away",
                        "trait": "conscientiousness",
                        "sentiment": "positive", 
                    },
                    {
                        "value": "I am easily disturbed",
                        "text": "I am easily disturbed",
                        "trait": "neuroticism",
                        "sentiment": "negative", 
                    },
                    {
                        "value": "I have excellent ideas",
                        "text": "I have excellent ideas",
                        "trait": "imagination",
                        "sentiment": "positive", 
                    },
                    { 
                        "value": "I have little to say",
                        "text": "I have little to say",
                        "trait": "extraversion",
                        "sentiment": "negative", 
                    },
                    {
                        "value": "I have a soft heart",
                        "text": "I have a soft heart",
                        "trait": "agreeableness",
                        "sentiment": "positive", 
                    },
                    {
                        "value": "I often forget to put things back in their proper place",
                        "text": "I often forget to put things back in their proper place",
                        "trait": "conscientiousness",
                        "sentiment": "negative", 
                    },
                    {
                        "value": "I get upset easily",
                        "text": "I get upset easily",
                        "trait": "neuroticism",
                        "sentiment": "negative", 
                    },
                    { 
                        "value": "I do not have a good imagination",
                        "text": "I do not have a good imagination",
                        "trait": "imagination",
                        "sentiment": "negative", 
                    },
                    {
                        "value": "I talk to a lot of different people at parties",
                        "text": "I talk to a lot of different people at parties",
                        "trait": "extraversion",
                        "sentiment": "positive", 
                    },
                    {
                        "value": "I am not really interested in others",
                        "text": "I am not really interested in others",
                        "trait": "agreeableness",
                        "sentiment": "negative", 
                    },
                    {
                        "value": "I like order",
                        "text": "I like order",
                        "trait": "conscientiousness",
                        "sentiment": "positive", 
                    },
                    {
                        "value": "I change my mood a lot",
                        "text": "I change my mood a lot",
                        "trait": "neuroticism",
                        "sentiment": "negative", 
                    },
                    { 
                        "value": "I am quick to understand things",
                        "text": "I am quick to understand things",
                        "trait": "imagination",
                        "sentiment": "positive", 
                    },
                    {
                        "value": "I don't like to draw attention to myself",
                        "text": "I don't like to draw attention to myself",
                        "trait": "extraversion",
                        "sentiment": "negative", 
                    },
                    {
                        "value": "I take time out for others",
                        "text": "I take time out for others",
                        "trait": "agreeableness",
                        "sentiment": "positive", 
                    },
                    {
                        "value": "I shirk my duties",
                        "text": "I shirk my duties",
                        "trait": "conscientiousness",
                        "sentiment": "negative", 
                    },
                    {
                        "value": "I have frequent mood swings",
                        "text": "I have frequent mood swings",
                        "trait": "neuroticism",
                        "sentiment": "negative", 
                    },
                    { 
                        "value": "I use difficult words",
                        "text": "I use difficult words",
                        "trait": "imagination",
                        "sentiment": "positive", 
                    },
                    {
                        "value": "I don't mind being the center of attention",
                        "text": "I don't mind being the center of attention",
                        "trait": "extraversion",
                        "sentiment": "positive", 
                    },
                    {
                        "value": "I feel others' neuroticisms",
                        "text": "I feel others' neuroticisms",
                        "trait": "agreeableness",
                        "sentiment": "positive", 
                    },
                    {
                        "value": "I follow a schedule",
                        "text": "I follow a schedule",
                        "trait": "conscientiousness",
                        "sentiment": "positive", 
                    },
                    {
                        "value": "I get irritated easily",
                        "text": "I get irritated easily",
                        "trait": "neuroticism",
                        "sentiment": "negative", 
                    },
                    { 
                        "value": "I spend time reflecting on things",
                        "text": "I spend time reflecting on things",
                        "trait": "imagination",
                        "sentiment": "positive", 
                    },
                    {
                        "value": "I am quiet around strangers",
                        "text": "I am quiet around strangers",
                        "trait": "extraversion",
                        "sentiment": "negative", 
                    },
                    {
                        "value": "I make people feel at ease",
                        "text": "I make people feel at ease",
                        "trait": "agreeableness",
                        "sentiment": "positive", 
                    },
                    {
                        "value": "I am exacting in my work",
                        "text": "I am exacting in my work",
                        "trait": "conscientiousness",
                        "sentiment": "positive", 
                    },
                    {
                        "value": "I often feel blue",
                        "text": "I often feel blue",
                        "trait": "neuroticism",
                        "sentiment": "negative", 
                    },
                    {
                        "value": "I am full of ideas",
                        "text": "I am full of ideas",
                        "trait": "imagination",
                        "sentiment": "positive", 
                    },
                ],
                "isRequired": True,
                "isAllRowRequired": True,
            },
        ],
    }
}

# values from paper
coef = {
    "risk_tolerance": {
        "constant": 2.936,
        "coef": {
            "age": -0.01,
            "gender": 0.421,
            "income": 0.386,
            "mediumEducation": 0.048,
            "highEducation": 0.096,
            "financeKnowledge": 0.09,
            "financeAdministrator": 0,
            "mainWageEarner": -0.012,
            "householdHead": -0.36,
            "spouse": -0.22,
            "extraversion": 0.125,
            "imagination": 0.121,
            "agreeableness": -0.176,
            "conscientiousness": -0.096,
            "neuroticism": -0.112,
        }
    },
    "savings_ratio": {
        "constant": 1.645,
        "coef": {
            "age": 0,
            "gender": -0.063,
            "income": -0.345,
            "mediumEducation": 0.059,
            "highEducation": 0.087,
            "financeKnowledge": -0.02,
            "financeAdministrator": 0.253,
            "mainWageEarner": -0.009,
            "householdHead": -0.729,
            "spouse": -0.851,
            "extraversion": -0.018,
            "imagination": 0.014,
            "agreeableness": -0.004,
            "conscientiousness": -0.01,
            "neuroticism": 0.018,
            "risk_tolerance": -0.066,
        }
    },
    "bond_and_mutual_fund_ratio": {
        "constant": -1.331,
        "coef": {
            "age": 0.009,
            "gender": 0.02,
            "income": 0.432,
            "mediumEducation": 0.044,
            "highEducation": 0.172,
            "financeKnowledge": 0.085,
            "financeAdministrator": 0.182,
            "mainWageEarner": -0.04,
            "householdHead": -0.07,
            "spouse": -0.072,
            "extraversion": -0.043,
            "imagination": 0.012,
            "agreeableness": -0.027,
            "conscientiousness": -0.018,
            "neuroticism": -0.024,
            "risk_tolerance": 0.078,
        }
    },
    "equity_ratio": {
        "constant": -2.049,
        "coef": {
            "age": 0.006,
            "gender": 0.097,
            "income": 0.412,
            "mediumEducation": 0.081,
            "highEducation": 0.091,
            "financeKnowledge": 0.125,
            "financeAdministrator": 0.067,
            "mainWageEarner": 0.053,
            "householdHead": 0.265,
            "spouse": 0.383,
            "extraversion": -0.002,
            "imagination": 0.011,
            "agreeableness": -0.001,
            "conscientiousness": -0.001,
            "neuroticism": -0.044,
            "risk_tolerance": 0.109,
        }
    },
}

@app.route("/")
def home():
    return "<h1>Questions</h1>"

@app.route("/api")
def api_home():
    return "<h1>API Home</h1>"

def predict(features, constant, coef):
    y = []
    x = []
    for k in coef.keys():
        y.append(coef[k])
        x.append(features[k])
    y = np.array(y)
    x = np.array(x)
    return constant + np.dot(x, y.T)

def map(input_num, input_start, input_end, output_start, output_end):
    if input_num < input_start or input_num > input_end:
        raise Exception(f"input_num: {input_num} not in range of {input_start}-{input_end}")
    elif input_start >= input_end:
        if input_start == input_end:
            raise Exception(f"input_start: {input_start} cannot equal the input_end: {input_end}")
        else:
            raise Exception(f"input_start: {input_start} cannot be less than the input_end: {input_end}")
    elif output_start >= output_end:
        if output_start == output_end:
            raise Exception(f"input_start: {output_start} cannot equal the input_end: {output_end}")
        else:
            raise Exception(f"input_start: {output_start} cannot be less than the input_end: {output_end}")

    slope = (output_end-output_start)/(input_end-input_start)
    val = output_start + slope*(input_num - input_start)
    return val

@app.route("/api/survey/<type>", methods=["GET", "POST"])
def survey(type):
    global stuff
    global coef
    stuff = request.headers
    if request.method == "GET":
        if type not in surveys:
            return jsonify(None), 404
        return jsonify(surveys[type])
    elif request.method == "POST":
        data = request.get_json()
        if type == "riskassessment": 
            features = data["questions"]
            scores = {}
            # print(data)
            personality_traits = data["traits"]
            min_num = 1
            max_num = 5
            personality_data = pd.DataFrame(features["personality"])
            # calculate personality score, for negative values we invert the mapping so 1 --> 5, ..., 5 --> 1
            # we can do that by min - val + max
            for trait in personality_traits:
                df_trait = personality_data[personality_data["trait"] == trait]
                num_questions = len(df_trait)
                df_positive = df_trait[df_trait["sentiment"] == "positive"]
                df_negative = df_trait[df_trait["sentiment"] == "negative"]
                invert_negative = min_num - df_negative["value"] + max_num
                col_score = (df_positive["value"].sum() + invert_negative.sum()) / num_questions
                scores[trait] = col_score
            features.pop("personality", None)
            features.update(scores)
            # converting features to numeric

            for k in list(features.keys()):
                if isinstance(features[k], bool):
                    features[k] = 1 if features[k] else 0  
                elif k == "income":
                    features[k] /= 100000 # paper says to do this
                elif k == "gender":
                    if features[k] == "male":
                        val = 1
                    elif features[k] == "other": # not in paper but have to be politically correct?
                        val = 0.5
                    else:
                        val = 0
                    features[k] = val
            risk_tolerance = predict(features, coef["risk_tolerance"]["constant"], coef["risk_tolerance"]["coef"])
            risk_tolerance = min(risk_tolerance, 7) # max val from paper
            risk_tolerance = max(risk_tolerance, 1) # min val from paper
            risk_tolerance = map(risk_tolerance, 1, 7, 0, 1) # map to 0 - 1
            risk_tolerance = round(risk_tolerance, 2)
            features["risk_tolerance"] = risk_tolerance
            print(features) # todo remove for prod
            
            # savings_ratio = max(0, predict(features, coef["savings_ratio"]["constant"], coef["savings_ratio"]["coef"]))
            # savings_ratio = predict(features, coef["savings_ratio"]["constant"], coef["savings_ratio"]["coef"])
            # bond_and_mutual_fund_ratio = max(0, predict(features, coef["bond_and_mutual_fund_ratio"]["constant"], coef["bond_and_mutual_fund_ratio"]["coef"]))
            # bond_and_mutual_fund_ratio = predict(features, coef["bond_and_mutual_fund_ratio"]["constant"], coef["bond_and_mutual_fund_ratio"]["coef"])
            # equity_ratio = max(0, predict(features, coef["equity_ratio"]["constant"], coef["equity_ratio"]["coef"]))
            # equity_ratio = predict(features, coef["equity_ratio"]["constant"], coef["equity_ratio"]["coef"])
            return jsonify({
                "personality": scores, 
                "features": features, 
                "risk_tolerance": risk_tolerance,
                # "savings_ratio": savings_ratio,
                # "bond_and_mutual_fund_ratio": bond_and_mutual_fund_ratio,
                # "equity_ratio": equity_ratio,
                })
        else:
            return jsonify(None), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('FLASK_APP_PORT'))

