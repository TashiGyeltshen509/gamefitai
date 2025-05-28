const data = {
  demo1: [
    "Step 1",
    "Start Playing (Access the Game Selection Page)",
    "Click “Play Now” on the Home Page OR go directly to the Game Selection Page.",
    "assets/images/WhatIsGameFitAi.jpg",
  ],
  demo2: [
    "Step 2",
    "Choose Your Game (Select Your Favorite Game)",
    "Pick a game from the supported list and click to open it!",
    "assets/images/WhatIsGameFitAi.jpg",
  ],
  demo3: [
    "Step 3",
    "Connect Your Hands to Start (AI Model Activation)",
    "Once the game opens, raise both hands in front of your webcam to activate motion tracking.",
    "assets/images/WhatIsGameFitAi.jpg",
  ],
  demo4: [
    "Step 4",
    "Control the Game with Your Body (Motion-Based Gameplay)",
    "Move to trigger in-game actions!",
    "assets/images/WhatIsGameFitAi.jpg",
  ],
  demo5: [
    "Step 5",
    "Exit the Game (Safely End the Session)",
    "To exit the game, press the “Escape” button on your keyboard.",
    "assets/images/WhatIsGameFitAi.jpg",
  ],
};

const buttons = document.querySelectorAll(".button");
const stepElement = document.querySelector(".content .step");
const titleElement = document.querySelector(".content .title");
const subtitleElement = document.querySelector(".content .subtitle");
const imgElement = document.querySelector(".img img");

buttons.forEach((button, index) => {
  button.addEventListener("click", () => {
    buttons.forEach((btn) => btn.classList.remove("active"));
    button.classList.add("active");

    const stepKey = `demo${index + 1}`;
    const stepData = data[stepKey];

    stepElement.style.animation = "none";
    titleElement.style.animation = "none";
    subtitleElement.style.animation = "none";
    imgElement.style.animation = "none";

    void stepElement.offsetWidth;

    setTimeout(() => {
      stepElement.textContent = stepData[0];
      titleElement.textContent = stepData[1];
      subtitleElement.textContent = stepData[2];
      imgElement.src = staticBasePath + stepData[3];

      stepElement.style.animation = "showContent 0.5s linear forwards";
      stepElement.style.animationDelay = "0.2s";

      titleElement.style.animation = "showContent 0.5s linear forwards";
      titleElement.style.animationDelay = "0.4s";

      subtitleElement.style.animation = "showContent 0.5s linear forwards";
      subtitleElement.style.animationDelay = "0.8s";

      imgElement.style.animation = "showImg 0.5s linear forwards";
    }, 50);
  });
});
