{% extends 'base.tpl' %}
{% load static %}

{% block stylesheets %}
    <link rel="stylesheet" href="{% static 'css/savedate.css' %}" type="text/css" />
{% endblock %}

{% block title %}My Page{% endblock %}

{% block beforecontainer %}
<div class="modal-background"></div>
{% endblock %}
{% block pagecontent %}
    <div class="save-the-date modal modal-fx-3dSign">
        <div class="modal-content">
            <h1 class="gold-script centered">Save the Date</h1>
            <h3 class="em centered bottom">Friday, September 18, 2020 | Vail, CO</h3>
        </div>
    </div>
    <div class="save-the-date modal modal-fx-3dSign">
        <div class="modal-content">
            <p>Why does this box hate me? We just want your email.</p>
            <form class="columns">
                <input type="email" class="input column" placeholder="email">
                <button class="button is-primary column">Send!</button>
            </form>
        </div>
        {#        <button class="modal-close is-large" aria-label="close"></button>#}
    </div>
    </div>
{% endblock %}
