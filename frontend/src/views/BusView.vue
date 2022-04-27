<template>
  <v-container>
    <v-data-table
      :headers="headers"
      :items="busesFinales"
      sort-by="license_plate"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Buses</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
          <v-dialog v-model="dialog" max-width="500px">
            <template v-slot:activator="{ on, attrs }">
              <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on">
                Nuevo Bus
              </v-btn>
            </template>

            <v-card>
              <v-card-title>
                <span class="text-h5">{{ formTitle }}</span>
              </v-card-title>

              <v-container>
                <form>
                  <v-text-field
                    v-model="licensePlateForm"
                    :error-messages="licensePlateFormErrors"
                    :counter="10"
                    label="Placa"
                    required
                    @input="$v.licensePlateForm.$touch()"
                    @blur="$v.licensePlateForm.$touch()"
                  ></v-text-field>
                  <v-select
                    v-model="selectDriverForm"
                    :items="driversList"
                    :error-messages="selectDriverFormErrors"
                    label="Selecciona al chofer"
                    required
                    @change="$v.selectDriverForm.$touch()"
                    @blur="$v.selectDriverForm.$touch()"
                  ></v-select>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="blue darken-1" text @click="close">
                      Cancelar
                    </v-btn>
                    <v-btn color="blue darken-1" text @click="submit">
                      {{ editedIndex === -1 ? "Crear" : "Editar" }}
                    </v-btn>
                  </v-card-actions>
                </form>
              </v-container>
            </v-card>
          </v-dialog>
          <v-dialog v-model="dialogDelete" max-width="500px">
            <v-card>
              <v-card-title class="text-h5"
                >Estás seguro de borrar este bus?</v-card-title
              >
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="closeDelete"
                  >Cancel</v-btn
                >
                <v-btn color="blue darken-1" text @click="deleteItemConfirm"
                  >OK</v-btn
                >
                <v-spacer></v-spacer>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-toolbar>
      </template>
      <template v-slot:item.actions="{ item }">
        <v-icon small class="mr-2" @click="editItem(item)"> mdi-pencil </v-icon>
        <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
      </template>
      <template v-slot:no-data>
        <v-container>
          <h1>No se registraron Buses</h1>
        </v-container>
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
import getAPI from "../api/busApi";
import { validationMixin } from "vuelidate";
import {
  required,
  maxLength,
  minLength,
  numeric,
} from "vuelidate/lib/validators";

export default {
  mixins: [validationMixin],

  validations: {
    licensePlateForm: { required, maxLength: maxLength(10), numeric },
    selectDriverForm: { required },
  },

  data: () => ({
    licensePlateForm: "",
    selectDriverForm: null,
    drivers: [],
    driversList: [],
    dialog: false,
    dialogDelete: false,
    headers: [
      {
        text: "Placa",
        align: "start",
        value: "license_plate",
      },
      { text: "Chofer", value: "driver" },
      { text: "Actions", value: "actions", sortable: false },
    ],
    buses: [],
    busesFinales: [],
    editedIndex: -1,
    currentBus: {
      id: null,
      license_plate: null,
      driver: null,
    },
    defaultBus: {
      id: null,
      license_plate: null,
      driver: null,
    },
    newBus: { license_plate: null, driver_id: null },
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "Nuevo Bus" : "Edit Bus";
    },
    licensePlateFormErrors() {
      const errors = [];
      if (!this.$v.licensePlateForm.$dirty) return errors;
      !this.$v.licensePlateForm.numeric &&
        errors.push("La placa solo contiene números");
      !this.$v.licensePlateForm.maxLength &&
        errors.push("La placa debe tener 10 caracteres");
      !this.$v.licensePlateForm.required &&
        errors.push("La placa es obligatoria.");
      return errors;
    },
    selectDriverFormErrors() {
      const errors = [];
      if (!this.$v.selectDriverForm.$dirty) return errors;
      !this.$v.selectDriverForm.required &&
        errors.push("Chofer es obligatorio");
      return errors;
    },
  },

  watch: {
    dialog(val) {
      val || this.close();
    },
    dialogDelete(val) {
      val || this.closeDelete();
    },
  },

  created() {
    this.initialize();
  },

  methods: {
    getBuses() {
      getAPI
        .get("/api/bus/")
        .then((response) => {
          console.log("load data");
          this.buses = response.data;
          this.busesFinales = this.buses.map((b) => {
            const { driver } = b;
            return {
              ...b,
              driver: `${driver.first_name} ${driver.last_name}`,
            };
          });
        })
        .catch((err) => {
          console.log(err);
        });
    },

    createBuses(bus) {
      getAPI
        .post("/api/bus/", bus)
        .then(() => {
          console.log("created bus");
          this.getDrivers();
          this.getBuses();
          this.newBus = {};
          this.resetForm();
          this.close();
        })
        .catch((err) => {
          console.log(err);
        });
    },

    updateBus(bus) {
      const { id } = this.currentBus;
      getAPI
        .put(`/api/bus/${id}/`, bus)
        .then(() => {
          console.log("edited bus");
          this.getBuses();
          this.getDrivers();
          this.newBus = {};
          this.resetForm();
          this.close();
        })
        .catch((err) => {
          console.log(err);
        });
    },

    deleteBuses() {
      const { id } = this.currentBus;
      getAPI
        .delete(`/api/bus/${id}/`)
        .then(() => {
          console.log("deleted bus");
          this.getBuses();
          this.resetForm();
          this.close();
        })
        .catch((err) => {
          console.log(err);
        });
    },

    getDrivers() {
      getAPI
        .get("/api/driver/")
        .then((response) => {
          console.log("load data");
          this.drivers = response.data.filter(d => d.is_working === false);
          this.driversList = this.drivers.map((d) => ({
            text: `${d.first_name} ${d.last_name}`,
            value: d.id,
          }));
        })
        .catch((err) => {
          console.log(err);
        });
    },

    initialize() {
      this.getBuses();
      this.getDrivers();
    },

    editItem(item) {
      this.editedIndex = this.busesFinales.indexOf(item);
      this.currentBus = this.buses.find(
        (b) => b.id === this.busesFinales[this.editedIndex].id
      );
      this.licensePlateForm = this.currentBus.license_plate;
      this.selectDriverForm = this.currentBus.driver.id;
      this.dialog = true;
    },

    deleteItem(item) {
      this.editedIndex = this.busesFinales.indexOf(item);
      this.currentBus = this.buses.find(
        (b) => b.id === this.busesFinales[this.editedIndex].id
      );
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      this.deleteBuses();
      this.closeDelete();
    },

    close() {
      this.dialog = false;
      this.resetForm();
      this.$nextTick(() => {
        this.currentBus = { ...this.defaultBus };
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.currentBus = { ...this.defaultBus };
        this.editedIndex = -1;
      });
    },

    submit() {
      this.$v.$touch();
      if (this.$v.$invalid) return;
      this.newBus.license_plate = this.licensePlateForm;
      this.newBus.driver_id = this.selectDriverForm;
      this.editedIndex === -1
        ? this.createBuses(this.newBus)
        : this.updateBus(this.newBus);
    },

    clear() {
      this.resetForm();
    },

    resetForm() {
      this.$v.$reset();
      this.licensePlateForm = "";
      this.selectDriverForm = null;
    },
  },
};
</script>

<style>
</style>