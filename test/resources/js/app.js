import '../scss/app.scss';
import 'bootstrap/dist/css/bootstrap.min.css';

import Axios from 'axios';
import Vue from 'vue';
import moment from 'moment';
import VueMoment from 'vue-moment';

require('moment/locale/es');

moment.locale('es');

Vue.use(VueMoment, (moment));

window.axios = Axios;

window.axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

let token = document.head.querySelector('meta[name="csrf_token"]');

if (token) {
    window.axios.defaults.headers.common['X-CSRFToken'] = token.content;
} else {
    console.error('CSRF token not found');
}


Vue.filter('formatDate', function (value) {
    if (value) {
        return moment(String(value)).format('MM/DD/YYYY hh:mm')
    }
});
window.Vue = Vue;
