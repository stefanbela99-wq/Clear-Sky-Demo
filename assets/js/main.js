/* Clear Sky Consulting - front-end interactions */
(function () {
  "use strict";

  // Mobile nav toggle
  var toggle = document.querySelector(".nav__toggle");
  var links = document.querySelector(".nav__links");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      links.classList.toggle("open");
    });
  }

  // Set current year in footer
  var yearEl = document.querySelectorAll("[data-year]");
  yearEl.forEach(function (el) { el.textContent = new Date().getFullYear(); });

  // Highlight active nav link based on current file
  var current = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".nav__links a:not(.btn)").forEach(function (a) {
    var href = a.getAttribute("href");
    if (href === current || (current === "" && href === "index.html")) {
      a.classList.add("active");
    }
  });

  /* ------------------------------------------------------------------
     Form handling (contact + application)
     These forms are wired for a static demo: on submit we show a
     success message. To receive real submissions, point the form's
     `action` at your provider (Formspree, Netlify Forms, or your own
     endpoint) and remove the preventDefault demo handler below.
  ------------------------------------------------------------------ */
  document.querySelectorAll("form[data-demo-form]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      // Basic native validation first
      if (!form.checkValidity()) return; // let the browser show messages
      e.preventDefault();
      var status = form.querySelector(".form-status");
      if (status) {
        status.classList.add("show");
        status.scrollIntoView({ behavior: "smooth", block: "center" });
      }
      form.reset();
    });
  });
})();
