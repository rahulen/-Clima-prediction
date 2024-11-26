$("#btn_savedata").click(function () {
  var uname = document.getElementById("nm").value;
  var email = document.getElementById("em").value;
  var phone = document.getElementById("ph").value;
  var gender = document.getElementById("gender").value;
  var address = document.getElementById("addr").value;
  var password = document.getElementById("pswd").value;
  var nmpattern = /^[a-zA-Z ]+$/;
  var phpattern = /^[6-9]{1}[0-9]{9}$/;
  var empattern = /^[a-z0-9]+@[a-z]+\.[a-z]{2,3}$/;
  var pswdpattern =
    /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{5,8}$/;

  if (uname == "") {
    alert("Please Enter Your Name");
    return false;
  }
  if (!nmpattern.test(uname)) {
    alert("Invalid Name");
    return false;
  }
  if (email == "") {
    alert("Please Enter Your Email");
    return false;
  }
  if (!empattern.test(email)) {
    alert("Invalid email id");
    return false;
  }
  if (phone == "") {
    alert("Please Enter Your Phone Number");
    return false;
  }
  if (!phpattern.test(phone)) {
    alert("Invalid phone");
    return false;
  }
  if (gender == "") {
    alert("Please Select Your Gender");
    return false;
  }

  if (password == "") {
    alert("Please Enter Password");
    return false;
  }

  if (!pswdpattern.test(password)) {
    alert("Enter correct password");
    return false;
  }

  $.ajax({
    type: "GET",
    url: "/regdata",
    contentType: "application/json;charset=UTF-8",
    data: {
      stname: uname,
      email: email,
      phone: phone,
      gender: gender,
      addr1: address,
      pswd: password,
    },
    dataType: "json",
    success: function (resp) {
      alert(resp);
      window.location = "login";
    },
    failure: function (resp) {
      alert("Data Saved Failed");
    },
  });
});

$("#btn_logindata").click(function () {
  var email = document.getElementById("em").value;
  var pswd = document.getElementById("pswd").value;

  var empattern = /^[a-z0-9]+@[a-z]+\.[a-z]{2,3}$/;

  if (email == "") {
    alert("Please Enter Your Email");
    return false;
  }
  if (!empattern.test(email)) {
    alert("Invalid email id");
    return false;
  }

  if (pswd == "") {
    alert("Please Enter Password");
    return false;
  }

  $.ajax({
    type: "GET",
    url: "/logdata",
    contentType: "application/json;charset=UTF-8",
    data: {
      email: email,
      pswd: pswd,
    },
    dataType: "json",
    success: function (resp) {
      if (resp == "success") {
        window.location = "dashboard";
      }
      if (resp == "failure") {
        alert("Credentials not found");
        window.location = "register";
      }
    },
    failure: function (resp) {
      alert("Data Fetch Failed");
    },
  });
});

$("#btn_reset_log").click(function () {
  window.location = "home";
});

$("#btn_reset_reg").click(function () {
  window.location = "register";
});

$("#btn_reset_predict").click(function () {
  window.location = "predict";
});

function sendData(data) {
  var meantemp = data["mean_temp"];
  var humidity = data["humidity"];
  document.getElementById("mean_temp").innerText = meantemp;
  document.getElementById("humidity").innerText = humidity;
}

$("#btn_predictdata").click(function () {
  var date = document.getElementById("date").value;

  if (date == "") {
    alert("Please Choose Date");
    return false;
  }

  $.ajax({
    type: "GET",
    url: "/predictdata",
    contentType: "application/json;charset=UTF-8",
    data: {
      date: date,
    },
    dataType: "json",
    success: function (resp) {
      sendData(resp);
    },
    failure: function (resp) {
      alert("Data prediction Failed");
    },
  });
});
