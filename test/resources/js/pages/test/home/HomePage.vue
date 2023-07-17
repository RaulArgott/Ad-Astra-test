<template>
  <div class="home-page">
    <h1 class="display-5 fw-bold text-center">
      Zones and Distributions
    </h1>

    <div class="col-lg-6 mx-auto zones mb">
      <zone-editable v-for="zone in zones" :id="zone.id" :name="zone.name" :updated_at="zone.updated_at"
        :distributions="zone.distributions" :key="zone.uid" @edit="save($event, zone)" @initLoading="showLoading()"
        @hideLoading="hideLoading()" class="zone" />
    </div>

    <h1 class="display-5 fw-bold text-center">
      To Do List
    </h1>

    <ul class="col-lg-6 mx-auto">
      <li>Add the percentage symbol to each distribution number while is not being edited DONE</li>
      <li>The cancel button is not working DONE</li>
      <li>Without refreshing the page, be able to edit all the distributions from a zone DONE</li>
      <li>Be able to add more distributions DONE</li>
      <li>Be able to remove distributions DONE</li>
      <li>When the user is not able to save due to some error, the error must be showed DONE</li>
      <li>The sum of all distributions must be ensured to be 100% in anyway DONE</li>
      <li>The distributions must be integer DONE</li>
      <li>The zone name cannot be empty DONE</li>
      <li>The zone name cannot have more than one space between each word DONE</li>
      <li>The zone name cannot have spaces at start or the end DONE</li>
      <li>The zone name cannot be repeated in any way DONE</li>
      <li>Create a new field "updated_at" that is going to store the date when the name field change DONE</li>
      <li>Show the updated_at field value near each zone name DONE</li>
      <li>Add a way for the user to know that an element is being saved DONE</li>
      <li>When the number of distributions is 5 or greater, the background of that zone must change to any color while is
        not being edited DONE</li>
    </ul>
    <loading-component v-if="loading"></loading-component>
  </div>
</template>

<script>
import ZoneEditable from './ZoneEditable.vue';
import LoadingComponent from '../../../components/Loading.vue';
export default {
  name: 'HomePage',
  components: {
    ZoneEditable,
    LoadingComponent
  },
  props: {
    context: {
      type: Object
    }
  },
  data() {
    return {
      zones: [],
      zoneUid: 0,
      loading: false,
    };
  },
  mounted() {
    this.zones = this.context.zones.map(data => {
      return {
        id: data.id,
        name: data.name,
        uid: this.zoneUid++,
        updated_at: data.updated_at,
        distributions: data.distributions
      };
    });
  },
  methods: {
    save($event, zone) {
      zone.name = $event.name;
      zone.distributions = $event.distributions;
      zone.updated_at = $event.updated_at;
    },
    showLoading() {
      this.loading = true;
    },
    hideLoading() {
      this.loading = false;
    }
  }
}
</script>

<style lang="scss">
@import 'resources/scss/variables.scss';

.home-page {
  .zones {
    display: flex;
    gap: 4px;
    flex-direction: column;
  }
}
</style>
