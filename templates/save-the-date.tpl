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
            <h1 id="bigtext">Save the Date</h1>
            <p>We would be delighted to welcome you to Vail, CO this September to celebrate.</p>
            <div class="columns">
              <div class="column">
                <form>
                <input type="email" class="input" placeholder="email">
                </form></div>
              <div class="column">
            <button class="button">Button</button>
            <button class="button is-primary">Primary button</button></div>
              <div class="column">4</div>
            </div>
        </div>
    </div>
{#    <div class="save-the-date two modal modal-fx-3dSign">#}
{#        <div class="modal-background"></div>#}
{#        <div class="modal-content">#}
{#            <h1 id="bigtext">Save the Date</h1>#}
{#            <p>We would be delighted to welcome you to Vail, CO this September to celebrate.#}
{#        </div>#}
{#        <button class="modal-close is-large" aria-label="close"></button>#}
{#    </div>#}
{% endblock %}
