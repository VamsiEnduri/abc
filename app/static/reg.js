console.log("reg form js loaded");

// // 🔹 Show / hide specialization based on role
// document.getElementById("role").addEventListener("change", (e) => {
//   const specSelect = document.getElementById("specialization");

//   if (e.target.value === "Doctor") {
//     specSelect.style.display = "block";
//   } else {
//     specSelect.style.display = "none";
//     specSelect.value = ""; // important: clear value for Patient
//   }
// });

// 🔹 Register button logic
document.getElementById("reg_btn").addEventListener("click", () => {

  const data = {
    n: document.getElementById("name").value,
    e: document.getElementById("email").value,
    ph: document.getElementById("phNum").value,
    p: document.getElementById("password").value,
    cp: document.getElementById("c_password").value,
    r: document.getElementById("role").value,
    s: document.getElementById("specialization").value
  };



  console.log("SENDING DATA:", data); // 🔍 debug

  fetch("http://127.0.0.1:8000/register/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  })
    .then(res => res.json())
    .then(res => {
      console.log(res);
      alert(res.msg || res.error);
    })
    .catch(err => console.log(err));
});
