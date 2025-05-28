const images = [
  {
    src: "/assets/images/img1.jpg",
    text: "Team Lead",
    test2: "Karma Tenzin",
    test3:
      "Steering the team with vision and coordination, ensuring smooth collaboration and progress.",
  },
  {
    src: "/assets/images/img2.jpg",
    text: "Machine Learning Lead",
    test2: "Wangchen Thinley",
    test3:
      "Integrating intelligent data-driven solutions to optimize performance and automation.",
  },
  {
    src: "/assets/images/img3.jpg",
    text: "Frontend Lead",
    test2: "Sagar Khadal",
    test3:
      "Bringing creativity and precision to the frontend, ensuring a polished and interactive design.",
  },
  {
    src: "/assets/images/img4.jpg",
    text: "Tech Stack Lead",
    test2: "Tashi Gyeltshen",
    test3:
      "Identifies and recommends the most efficient technologies and tools to ensure optimal performance, scalability, and alignment with project goals.",
  },
  {
    src: "/assets/images/img5.jpg",
    text: "UI/UX Lead Designer",
    test2: "Garab Phuntsho Wangyel",
    test3:
      "Crafting seamless and intuitive user experiences, making sure every interaction feels natural and engaging.",
  },
];

let selectedIndex = 2;

function updateSlider() {
  const container = document.getElementById("thumbnail-container");
  const dotsContainer = document.getElementById("nav-dots");
  container.innerHTML = "";
  dotsContainer.innerHTML = "";

  const active = images[selectedIndex];
  const nextIndex = (selectedIndex + 1) % images.length;
  const next = images[nextIndex];

  // Active image
  const activeImg = document.createElement("img");
  activeImg.src =staticBasePath + active.src;
  activeImg.className = "thumbnail active";
  container.appendChild(activeImg);

  // Next image
  const nextImg = document.createElement("img");
  nextImg.src =staticBasePath + next.src;
  nextImg.className = "thumbnail";
  nextImg.onclick = () => {
    selectedIndex = nextIndex;
    updateSlider();
  };
  container.appendChild(nextImg);

  // Text
  document.getElementById("image-text").innerText = active.text;
  document.getElementById("image-text2").innerText = active.test2;
  document.getElementById("image-text3").innerText = active.test3;

  // Dots
  images.forEach((_, i) => {
    const dot = document.createElement("span");
    dot.className = i === selectedIndex ? "active" : "";
    dot.onclick = () => {
      selectedIndex = i;
      updateSlider();
    };
    dotsContainer.appendChild(dot);
  });
}

window.onload = updateSlider;
