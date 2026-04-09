// ================= EMOTIONS =================
CREATE (anxiety:Emotion {name: "Anxiety"})
CREATE (stress:Emotion {name: "Stress"})
CREATE (depression:Emotion {name: "Depression"})
CREATE (fatigue:Emotion {name: "Fatigue"})
CREATE (burnout:Emotion {name: "Burnout"})
CREATE (overthinking:Emotion {name: "Overthinking"})
CREATE (loneliness:Emotion {name: "Loneliness"})
CREATE (anger:Emotion {name: "Anger"})
CREATE (fear:Emotion {name: "Fear"})
CREATE (lowSelfEsteem:Emotion {name: "Low Self-Esteem"})

// ================= SYMPTOMS =================
CREATE (insomnia:Symptom {name: "Insomnia"})
CREATE (lowFocus:Symptom {name: "Low Focus"})
CREATE (lowEnergy:Symptom {name: "Low Energy"})
CREATE (restlessness:Symptom {name: "Restlessness"})
CREATE (irritability:Symptom {name: "Irritability"})
CREATE (mentalFog:Symptom {name: "Mental Fog"})
CREATE (headache:Symptom {name: "Headache"})
CREATE (sadness:Symptom {name: "Sadness"})
CREATE (negativeThinking:Symptom {name: "Negative Thinking"})
CREATE (lackMotivation:Symptom {name: "Lack of Motivation"})
CREATE (panic:Symptom {name: "Panic"})
CREATE (muscleTension:Symptom {name: "Muscle Tension"})

// ================= BEHAVIOURS =================
CREATE (procrastination:Behavior {name: "Procrastination"})
CREATE (socialWithdrawal:Behavior {name: "Social Withdrawal"})
CREATE (doomscrolling:Behavior {name: "Doomscrolling"})
CREATE (overworking:Behavior {name: "Overworking"})
CREATE (avoidance:Behavior {name: "Avoidance"})
CREATE (overthinkingBehavior:Behavior {name: "Overthinking Behavior"})

// ================= TECHNIQUES =================
CREATE (meditation:Technique {name: "Meditation"})
CREATE (breathing:Technique {name: "Breathing Exercise"})
CREATE (journaling:Technique {name: "Journaling"})
CREATE (walking:Technique {name: "Walking"})
CREATE (yoga:Technique {name: "Yoga"})
CREATE (pomodoro:Technique {name: "Pomodoro Technique"})
CREATE (sleepRoutine:Technique {name: "Sleep Routine"})
CREATE (digitalDetox:Technique {name: "Digital Detox"})
CREATE (gratitude:Technique {name: "Gratitude Practice"})
CREATE (powerNap:Technique {name: "Power Nap"})
CREATE (hydration:Technique {name: "Hydration"})
CREATE (exercise:Technique {name: "Exercise"})
CREATE (musicTherapy:Technique {name: "Music Therapy"})
CREATE (talkFriend:Technique {name: "Talk to Friend"})
CREATE (reading:Technique {name: "Reading"})
CREATE (mindfulness:Technique {name: "Mindfulness"})
CREATE (cbt:Technique {name: "Cognitive Restructuring"})
CREATE (exposure:Technique {name: "Exposure Therapy"})
CREATE (timeManagement:Technique {name: "Time Management"})
CREATE (goalSetting:Technique {name: "Goal Setting"})

// ================= BENEFITS =================
CREATE (calmMind:Benefit {name: "Calm Mind"})
CREATE (betterSleep:Benefit {name: "Better Sleep"})
CREATE (focusImprove:Benefit {name: "Improved Focus"})
CREATE (energyBoost:Benefit {name: "Increased Energy"})
CREATE (stressRelief:Benefit {name: "Stress Relief"})
CREATE (emotionalBalance:Benefit {name: "Emotional Balance"})
CREATE (confidence:Benefit {name: "Improved Confidence"})
CREATE (clarity:Benefit {name: "Mental Clarity"})
CREATE (resilience:Benefit {name: "Resilience"})
CREATE (motivation:Benefit {name: "Motivation"})

// ================= LIFESTYLE =================
CREATE (healthyRoutine:Lifestyle {name: "Healthy Routine"})
CREATE (socialConnection:Lifestyle {name: "Social Connection"})
CREATE (workLifeBalance:Lifestyle {name: "Work-Life Balance"})
CREATE (selfCare:Lifestyle {name: "Self Care"})

// ================= RELATIONS =================

// Emotion → Symptom
CREATE (anxiety)-[:CAUSES]->(panic)
CREATE (anxiety)-[:CAUSES]->(insomnia)
CREATE (stress)-[:CAUSES]->(lowFocus)
CREATE (stress)-[:CAUSES]->(headache)
CREATE (depression)-[:CAUSES]->(sadness)
CREATE (depression)-[:CAUSES]->(lowEnergy)
CREATE (fatigue)-[:CAUSES]->(mentalFog)
CREATE (burnout)-[:CAUSES]->(lowEnergy)
CREATE (overthinking)-[:CAUSES]->(negativeThinking)
CREATE (anger)-[:CAUSES]->(irritability)

// Symptom → Behavior
CREATE (lowFocus)-[:LEADS_TO]->(procrastination)
CREATE (sadness)-[:LEADS_TO]->(socialWithdrawal)
CREATE (negativeThinking)-[:LEADS_TO]->(overthinkingBehavior)
CREATE (lowEnergy)-[:LEADS_TO]->(avoidance)
CREATE (stress)-[:LEADS_TO]->(doomscrolling)

// Behavior → Technique
CREATE (procrastination)-[:MANAGED_BY]->(pomodoro)
CREATE (socialWithdrawal)-[:MANAGED_BY]->(talkFriend)
CREATE (doomscrolling)-[:MANAGED_BY]->(digitalDetox)
CREATE (overworking)-[:MANAGED_BY]->(workLifeBalance)
CREATE (avoidance)-[:MANAGED_BY]->(goalSetting)

// Symptom → Technique
CREATE (insomnia)-[:TREATED_BY]->(sleepRoutine)
CREATE (insomnia)-[:TREATED_BY]->(meditation)
CREATE (lowFocus)-[:TREATED_BY]->(mindfulness)
CREATE (mentalFog)-[:TREATED_BY]->(reading)
CREATE (irritability)-[:TREATED_BY]->(breathing)
CREATE (panic)-[:TREATED_BY]->(breathing)

// Emotion → Technique
CREATE (anxiety)-[:IMPROVES]->(breathing)
CREATE (stress)-[:IMPROVES]->(meditation)
CREATE (depression)-[:IMPROVES]->(walking)
CREATE (burnout)-[:IMPROVES]->(digitalDetox)
CREATE (overthinking)-[:IMPROVES]->(journaling)

// Technique → Benefit
CREATE (meditation)-[:LEADS_TO]->(calmMind)
CREATE (breathing)-[:LEADS_TO]->(calmMind)
CREATE (sleepRoutine)-[:LEADS_TO]->(betterSleep)
CREATE (pomodoro)-[:LEADS_TO]->(focusImprove)
CREATE (walking)-[:LEADS_TO]->(energyBoost)
CREATE (exercise)-[:LEADS_TO]->(energyBoost)
CREATE (journaling)-[:LEADS_TO]->(emotionalBalance)
CREATE (gratitude)-[:LEADS_TO]->(confidence)
CREATE (mindfulness)-[:LEADS_TO]->(clarity)
CREATE (cbt)-[:LEADS_TO]->(resilience)

// Benefit → Lifestyle
CREATE (calmMind)-[:SUPPORTS]->(selfCare)
CREATE (betterSleep)-[:SUPPORTS]->(healthyRoutine)
CREATE (focusImprove)-[:SUPPORTS]->(workLifeBalance)
CREATE (emotionalBalance)-[:SUPPORTS]->(socialConnection)
CREATE (r:Symptom {name: "Restlessness"})