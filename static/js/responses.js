function getBotResponse(input) {
    //rock paper scissors
    if (input == "how to use this app" || input=="how to use this website") {
        return "To use the predictor click on top right button, if you're a new user/doctor->Sign Up, otherwise->login. After successful login, You'll be redirected to the app where you've to enter all details as specified.";
    } else if (input == "what details to give") {
        return "Details needed are- name, age, cholestrol level, gender, thal,etc.";
    } else if (input == "how to get doctor consultation" || input=="how to talk to doctor" || input=="how to consult doctor") {
        return "Go to consultaion button from navbar and check for availabe doctor appointments. After checking availability, you can access doctor's details and contact them through email or directly have a one-one chat through chat app.";
    } else if (input == "symptoms of heart disease?") {
        return "There are 4 common symptoms like unusual fatigue, shoulder pain, chest pain,shortness of breath. For more check here: "
    } else if (input == "what are some precautions to avoid heart disease?" || input=="how to prevent heart disease") {
        return "Avoid alcoholic beverages, Avoid Stress, Eat Healthy food, Get enough sleep, Excercise or physical activity"
    } else if(input == "types of heart disease") {
        return "Coronary Artery Disease (CAD).\n Heart Arrhythmias.\n Heart Failure.\n Heart Valve Disease.\n Pericardial Disease.\n Cardiomyopathy (Heart Muscle Disease).Congenital Heart Disease."
    }

    // Simple responses
    if (input == "hello" || input == "hey"||input == "Hello"|| input == "hii" || input == "Hey") {
        return "Hello there!";
    } else if (input == "goodbye" ||input == "bye" ) {
        return "Talk to you later!";
    } else {
        return "Try asking something else!";
    }

}
