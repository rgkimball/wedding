{% extends 'base.tpl' %}
{% load static %}

{% block stylesheets %}
    <link rel="stylesheet" href="{% static 'css/savedate.css' %}" type="text/css" />
{% endblock %}

{% block title %}My Page{% endblock %}

{% block pagecontent %}
    <div class="save-the-date one modal modal-fx-3dSign">
        <div class="modal-background"></div>
        <div class="modal-content">
            <h1 class="gold-script centered">Save the Date</h1>
            <h3 class="em centered bottom">September 8, 2020 | Vail, CO</h3>
        </div>
    </div>
    <div class="save-the-date two modal modal-fx-3dSign">
        <div class="modal-background"></div>
        <div class="modal-content">
            <form>
                <input type="email" class="input" placeholder="email">
                <button class="button is-primary">Primary button</button>
            </form>
        </div>
        <button class="modal-close is-large" aria-label="close"></button>
    </div>
{% endblock %}
