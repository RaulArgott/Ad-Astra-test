<template>
  <div class="zone-editable" :class="isMoreThenFive">
    <div v-if="display" class="zone-display">
      <div>
        Zone Name: <strong>{{ name }}</strong> <span>({{ updated_at | formatDate }})</span> Distributions: {{
          distributionDisplay }}
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
            <input v-model="distribution.percentage" placeholder="Percentage" class="form-control" type="number" min="0"
              max="100" step="1">
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
    updated_at: String,
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
      /* Reset to delete elements */
      this.distributions_to_delete = [];
    },
    setDisplay(value) {
      /* Switch display aux */
      this.display = value;

      if (!this.display) {
        this.getValuesFromProps();
      }
    },
    save() {
      if (this.validate()) {
        this.saving = true;
        /* Creating object for api consumption */
        const params = {
          id: this.id,
          name: this.form.name.trimEnd().trimStart(),
          distributions: this.form.distributions,
          distributions_delete: this.distributions_to_delete,
        };
        /* Emit loading events while api consumption */
        this.$emit('initLoading');
        axios.post('/api/zones/edit', params)
          .then((res) => {
            let zoneRes = res.data[0];
            this.getValuesFromProps();
            this.$emit('edit', { name: params.name, distributions: zoneRes.distributions, updated_at: zoneRes.updated_at });
            this.display = true;
            this.$toastr.s('Guardado');
          }).catch((err) => {
            this.$toastr.e(err.response.data);
          }).finally(() => {
            this.saving = false;
            this.$emit('hideLoading');
          });
      }
    },
    addDistribution() {
      this.form.distributions.push({
        id: -1,
        percentage: null
      });
    },
    removeDistribution(index) {
      /* Remove from array and add to "To delete" elements */
      this.distributions_to_delete.push(this.form.distributions.splice(index, 1)[0].id);
    },
    isInt(n) {
      return n % 1 === 0;
    },
    validate() {
      /* Validate */
      let errs = []
      if (this.form.name.length < 1)
        errs.push('Name is required');
      if (this.form.name.includes('  '))
        errs.push('Name must not contain two spaces');
      if (this.form.distributions.length < 1)
        errs.push('At least 1 distribution is required');


      (this.form.distributions).forEach(dis => {
        if (!dis.percentage)
          dis.percentage = 0;
        if (!this.isInt(dis.percentage))
          errs.push(dis.percentage + ' is not an integer');
      });

      if (this.form.distributions.map(x => parseFloat(x.percentage)).reduce((a, b) => a + b) != 100)
        errs.push('Sum of distributions must be 100');

      (errs).forEach(element => {
        this.$toastr.e(element);
      });
      if (errs.length > 0)
        return false;
      return true;
    },
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
