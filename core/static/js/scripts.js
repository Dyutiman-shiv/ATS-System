function validateFormPosition(e, t, o, n, l, r, currentCTC, expectedCTC, currentLocation, noticePeriod, willingToRelocate) {
  var a = document.getElementById(t).value,
    // s = document.getElementById(o).value,
    i = document.getElementById(n).value,
    u = document.getElementById(l).files,
    c = document.getElementById(e),
    d = document.getElementById(r),
    m = validateName(t, a),
    cCTC = document.getElementById(currentCTC).value,
    eCTC = document.getElementById(expectedCTC).value,
    isCCTC = validateName(currentCTC, cCTC),
    isECTC = validateName(expectedCTC, eCTC),
    cLocation = document.getElementById(currentLocation).value,
    isLocation = validateName(currentLocation, cLocation),
    nPeriod = document.getElementById(noticePeriod).value,
    isPeriod = validateName(noticePeriod, nPeriod),
    toRelocation = document.getElementById(willingToRelocate).value,
    isWillingToRelocate = validateName(willingToRelocate, toRelocation);
  // y = validatePosition(o, s),
  p = validateCv(l, u),
    f = validatePhone(n, i);
  if (m && p && f && isCCTC && isECTC && isLocation && isPeriod && isWillingToRelocate) {
    d.innerHTML = "";
    var g = document.createElement("div");
    g.classList.add("loader"),
      d.appendChild(g),
      (d.disbaled = !0),
      submitFormPosition(t, o, n, l, currentCTC, expectedCTC, currentLocation, noticePeriod, willingToRelocate).then((e) => {
        openmodalApply(r, e), (c.style.display = "none");
        d.disbaled = false;
        d.innerHTML = "Submit";
      });
  }
}
function openmodalApply(e, t) {
  ("submitButtonApply" == e || "submitButtonApply2" == e) &&
    Swal.fire({
      title: `${t ? "Thanks for applying." : "Something went wrong."}`,
      text: `${t ? "Someone from our team will contact you." : "Please try again."}`,
      confirmButtonText: `<h6 class='d-flex mb-0' style='font-size:14px'><i class="bi bi-linkedin me-2"></i>Follow us on LinkedIn for Jobs Updates </h6>`,
      icon: `${t ? "success" : "error"}`,
      customClass: {
        confirmButton: 'p-3',
      },
      showCloseButton: true,
    }).then((e) => {
      if (e.isConfirmed) {
        window.location.href = 'https://www.linkedin.com/company/launchxin/';
      } else if (e.dismiss && t) {
        window.location.href = '/';
      }
      Swal.close();
      $('#exampleModalApply').modal('hide');
    })
}
function submitFormPosition(e, t, o, n, currentCTC, expectedCTC, currentLocation, noticePeriod, willingToRelocate) {
  var l = document.getElementById(e).value,
    a = document.getElementById(o).value,
    s = document.getElementById(n).files[0],
    cCTC = document.getElementById(currentCTC).value,
    eCTC = document.getElementById(expectedCTC).value,
    cLocation = document.getElementById(currentLocation).value,
    nPeriod = document.getElementById(noticePeriod).value,
    toRelocate = document.getElementById(willingToRelocate).value;


  i = new FormData();
  return (
    i.append("Name", l),
    i.append("Position", t),
    i.append("Phone", a),
    i.append("CV", s),
    i.append("cCTC", cCTC + ' LPA'),
    i.append("eCTC", eCTC + ' LPA'),
    i.append("cLocation", cLocation),
    i.append("nPeriod", nPeriod),
    i.append("toRelocate", toRelocate),
    fetch("/about/apply", { method: "POST", body: i })
      .then((e) => {
        if (!e.ok) throw Error("Network response was not ok");
        return e.text();
      })
      .then((e) => !0)
      .catch((e) => (console.error("Error:", e), !1))
  );
}
function validatePosition(e, t) {
  return t
    ? ((document.getElementById(e).style.borderColor = ""), !0)
    : ((document.getElementById(e).style.borderColor = "red"), !1);
}
function validateCv(e, t) {
  return 0 == t.length
    ? ((document.getElementById(e).style.borderColor = "red"), !1)
    : ((document.getElementById(e).style.borderColor = ""), !0);
}
function validateForm(e, t, o, n, l, r) {
  var a = document.getElementById(t).value,
    s = document.getElementById(o).value,
    i = document.getElementById(n).value,
    u = document.getElementById(l).value,
    c = document.getElementById(e),
    d = document.getElementById(r),
    m = validateName(t, a),
    y = validateEmail(o, s),
    p = validateComment(l, u),
    f = validatePhone(n, i);
  if (m && y && p && f) {
    d.innerText = "";
    var g = document.createElement("div");
    g.classList.add("loader"),
      d.appendChild(g),
      (d.disbaled = !0),
      submitForm(t, o, n, l).then((t) => {
        openmodal(r, t), "exampleModalMain" !== e && (c.style.display = "none");
      });
  }
}


function openmodal(e, t) {
  "submitButton1" == e &&
    Swal.fire({
      title: `${t ? "Thanks for sharing your details" : "Something went wrong"
        } `,
      text: `${t
        ? "Someone from our team will contact you soon."
        : "Please try again later."
        }`,
      icon: `${t ? "success" : "error"}`,
      customClass: {
        icon: 'h-25 w-25',
        popup: "your-popup-class",
        title: "your-title-class",
        content: "your-content-class",
        confirmButton: "your-confirm-button-class",
        cancelButton: "your-cancel-button-class",
      },
    }).then((e) => {
      e.isConfirmed && location.reload();
    }),
    "submitButton2" == e &&
    Swal.fire({
      title: `${t ? "Thanks for sharing your details" : "Something went wrong"
        } `,
      text: `${t
        ? "Someone from our team will contact you soon."
        : "Please try again later."
        }`,
      icon: `${t ? "success" : "error"}`,
      customClass: {
        popup: "your-popup-class",
        title: "your-title-class",
        content: "your-content-class",
        confirmButton: "your-confirm-button-class",
        cancelButton: "your-cancel-button-class",
      },
    }).then((e) => {
      e.isConfirmed && location.reload();
    }),
    "submitButton3" == e &&
    Swal.fire({
      title: `${t ? "Thanks for sharing your details" : "Something went wrong"
        } `,
      text: `${t
        ? "Someone from our team will contact you soon."
        : "Please try again later."
        }`,
      icon: `${t ? "success" : "error"}`,
      customClass: {
        popup: "your-popup-class",
        title: "your-title-class",
        content: "your-content-class",
        confirmButton: "your-confirm-button-class",
        cancelButton: "your-cancel-button-class",
      },
    }).then((e) => {
      e.isConfirmed && location.reload();
    }),
    "submitButtonApply" == e &&
    Swal.fire({
      title: "Thanks for sharing your details",
      text: "Someone from our team will contact you soon",
      icon: "success",
      customClass: {
        popup: "your-popup-class",
        title: "your-title-class",
        content: "your-content-class",
        confirmButton: "your-confirm-button-class",
        cancelButton: "your-cancel-button-class",
      },
    }).then((e) => {
      e.isConfirmed && location.reload();
    }),
    "submitButtonApply2" == e &&
    Swal.fire({
      title: "Thanks for sharing your details",
      text: "Someone from our team will contact you soon",
      icon: "success",
      customClass: {
        popup: "your-popup-class",
        title: "your-title-class",
        content: "your-content-class",
        confirmButton: "your-confirm-button-class",
        cancelButton: "your-cancel-button-class",
      },
    }).then((e) => {
      e.isConfirmed && location.reload();
    });
}
function submitForm(e, t, o, n) {
  var l = document.getElementById(e).value,
    r = document.getElementById(t).value,
    a = document.getElementById(o).value,
    s = document.getElementById(n).value,
    i = new FormData();
  return (
    i.append("name", l),
    i.append("email", r),
    i.append("phone", a),
    i.append("message", s),
    fetch("/about/lead", { method: "POST", body: i })
      .then((e) => {
        if (!e.ok) throw Error("Network response was not ok");
        return e.text();
      })
      .then((e) => !0)
      .catch((e) => (console.error("Error:", e), !1))
  );
}
function validateComment(e, t) {
  return 0 == t.length
    ? ((document.getElementById(e).style.borderColor = "red"), !1)
    : ((document.getElementById(e).style.borderColor = ""), !0);
}
function validatePhone(e, t) {
  return t.length < 10 || /\D/.test(t)
    ? ((document.getElementById(e).style.borderColor = "red"), !1)
    : ((document.getElementById(e).style.borderColor = ""), !0);
}
function validateName(e, t) {
  return 0 == t.length
    ? ((document.getElementById(e).style.borderColor = "red"), !1)
    : ((document.getElementById(e).style.borderColor = ""), !0);
}
function validateCTC(e, t) {
  return 0 == t.length
    ? ((document.getElementById(e).style.borderColor = "red"), !1)
    : ((document.getElementById(e).style.borderColor = ""), !0);
}
function validateEmail(e, t) {
  var o = document.getElementById(e),
    n = t.trim().toLowerCase(),
    l = t.lastIndexOf("@"),
    r = t.substring(l + 1);
  return l <= 0 || l === n.length - 1
    ? ((o.innerHTML = "Invalid email format"),
      (o.style.color = ""),
      (o.style.borderColor = "red"),
      !1)
    : ["gmail.com", "yahoo.com", "rediff.com", "hotmail.com"].includes(r)
      ? ((o.style.borderColor = "red"), !1)
      : ((o.style.borderColor = ""), (o.style.color = "black"), !0);
}
function closeButton() {
  location.reload();
}
