{% load static %}
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>
      Kathryn & Rob - {% block title %}{% endblock %}
    </title>

    <script src="{% static 'js/main.js' %}"></script>
    {% block scripts %}{% endblock %}
    <link rel="stylesheet" href="{% static 'css/main.css' %}" type="text/css" />
    <link rel="icon" href="{% static 'img/favicon.png' %}" type="image/x-icon" />
    {% block stylesheets %}{% endblock %}
  </head>
  <body>
    <div class="container">
      <h1>{% block heading %}{% endblock %}</h1>
      {% block pagecontent %}
      {% endblock %}
    </div>
    {% block footerscripts %}{% endblock %}
  </body>
</html>
