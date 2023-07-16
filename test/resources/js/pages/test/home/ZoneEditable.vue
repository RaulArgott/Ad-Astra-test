<template>
  <div class="zone-editable" :class="isMoreThenFive">
    <div v-if="display" class="zone-display">
      <div>
        Zone Name: <strong>{{ name }}</strong> Distributions: {{ distributionDisplay }}
      </div>

      <button class="btn btn-primary" @click="setDisplay(false)" :disabled="saving">
        Edit
      </button>
    </div>
    <div v-else class="zone-edit">
      <label class="control-label">
        Zone Name
      </label>

      <input v-model="form.name" placeholder="Zone name" class="form-control" :disabled="saving">

      <div class="zone-edit-distributions">
        <div v-for="(distribution, index) in form.distributions">
          <label class="control-label">
            Distribution
          </label>
          <div class="input-group">
            <input v-model="distribution.percentage" placeholder="Percentage" class="form-control">
            <button class="btn btn-danger" @click="removeDistribution(index)">
              <i class="fa-solid fa-trash-can"></i>
            </button>
          </div>
        </div>
      </div>

      <div class="zone-edit-actions">
        <button class="btn btn-outline-primary" @click="addDistribution()">
          Add distribution
        </button>

        <button class="btn btn-secondary" :disabled="saving" @click="setDisplay(true)">
          Cancel
        </button>

        <button class="btn btn-success" @click="save" :disabled="saving">
          Save
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ZoneEditable',
  props: {
    name: String,
    id: Number,
    distributions: Array,
  },
  data() {
    return {
      display: true,
      form: {
        name: '',
        distributions: [],
      },
      saving: false,
      distributions_to_delete: []
    };
  },
  computed: {
    distributionDisplay() {
      return this.distributions.map(distribution => '%' + distribution.percentage).join('-');
    },
    isMoreThenFive() {
      return this.distributions.length >= 5 && this.display ? 'five-or-more' : '';
    }
  },
  mounted() {
    this.getValuesFromProps();
  },
  methods: {
    getValuesFromProps() {
      this.form.name = this.name;
      this.form.distributions = this.distributions.map(distribution => {
        return {
          id: distribution.id,
          percentage: distribution.percentage
        };
      });
      this.distributions_to_delete = [];
    },
    setDisplay(value) {
      /* Switch display aux */
      this.display = value;

      if (!this.display) {
        this.getValuesFromProps();
      }
    },
    async save() {
      this.saving = true;
      /* Creating object for api consumption */
      const params = {
        id: this.id,
        name: this.form.name,
        distributions: this.form.distributions,
        distributions_delete: this.distributions_to_delete,
      };
      /* Emit loading events while api consumption */
      this.$emit('initLoading');
      const edited_distributions = await axios.post('/api/zones/edit', params);
      this.$emit('edit', { name: params.name, distributions: edited_distributions.data });
      this.$emit('hideLoading');

      /* Displaying aux variables */
      this.saving = false;
      this.display = true;
    },
    addDistribution() {
      this.form.distributions.push({
        id: -1,
        percentage: null
      });
    },
    removeDistribution(index) {
      this.distributions_to_delete.push(this.form.distributions.splice(index, 1)[0].id);
    }
  }
}
</script>

<style lang="scss">
@import 'resources/scss/variables.scss';

.zone-editable {
  border: 1px solid $gray-color;
  padding: $qmb;
  border-radius: $border-radius;

  .zone-display {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .zone-edit {
    display: flex;
    flex-direction: column;
    gap: $small-action-space;

    .zone-edit-actions {
      display: flex;
      gap: $small-action-space;
      justify-content: end;
    }

    .zone-edit-distributions {
      display: grid;
      grid-template-columns: repeat(1, 1fr);
      gap: $small-action-space;
    }

  }
}

.five-or-more {
  background-color: aqua;
}
</style>
