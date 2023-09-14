  $(document).ready(function() {
    $("#submitBtn").click(function() {
      var fullname = $("#fullname").val();
      var email = $("#email").val();
      var vehicle = $("#vehicle").val();

      $.ajax({
        type: "POST",
        url: "/driver_signup_ajax",
        data: {
          fullname: fullname,
          email: email,
          vehicle: vehicle
        },
        success: function(response) {
          $("#message").html(response.message).addClass(response.status);
          // Clear form inputs
          $("#fullname, #email, #vehicle").val("");
        }
      });
    });
  });

