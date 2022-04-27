<template>
  <v-container>
    <v-data-table
      :headers="headers"
      :items="destinationsFinales"
      sort-by="departure_place"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Trayectos</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
          <v-dialog v-model="dialog" max-width="500px">
            <template v-slot:activator="{ on, attrs }">
              <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on">
                Nuevo Trayecto
              </v-btn>
            </template>

            <v-card>
              <v-card-title>
                <span class="text-h5">{{ formTitle }}</span>
              </v-card-title>

              <v-container>
                <form>
                  <v-text-field
                    v-model="departurePlaceForm"
                    :error-messages="departurePlaceFormErrors"
                    :counter="20"
                    label="Punto de partida"
                    required
                    @input="$v.departurePlaceForm.$touch()"
                    @blur="$v.departurePlaceForm.$touch()"
                  ></v-text-field>
                  <v-text-field
                    v-model="arrivalPlaceForm"
                    :error-messages="arrivalPlaceFormErrors"
                    :counter="20"
                    label="Punto de llegada"
                    required
                    @input="$v.arrivalPlaceForm.$touch()"
                    @blur="$v.arrivalPlaceForm.$touch()"
                  ></v-text-field>
                  <v-text-field
                    v-model="scheduleDateForm"
                    type="datetime-local"
                    :error-messages="scheduleDateFormErrors"
                    label="Escoge un horario"
                    required
                    @input="$v.scheduleDateForm.$touch()"
                    @blur="$v.scheduleDateForm.$touch()"
                  ></v-text-field>
                  <!-- <v-menu
                    v-model="menu2"
                    :close-on-content-click="false"
                    max-width="290"
                  >
                    <template v-slot:activator="{ on, attrs }">
                      <v-text-field
                        :value="scheduleDateForm"
                        clearable
                        label="Seleccione una fecha"
                        readonly
                        v-bind="attrs"
                        v-on="on"
                        @click:clear="scheduleDateForm = null"
                      ></v-text-field>
                    </template>
                    <v-date-picker
                      v-model="scheduleDateForm"
                      @change="menu2 = false"
                    ></v-date-picker>
                  </v-menu> -->
                  <v-select
                    v-model="selectBusForm"
                    :items="busesList"
                    :error-messages="selectBusFormErrors"
                    label="Selecciona el trayecto"
                    required
                    @change="$v.selectBusForm.$touch()"
                    @blur="$v.selectBusForm.$touch()"
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
                >Estás seguro de borrar este trayecto?</v-card-title
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
          <h1>No se registraron Trayectos</h1>
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
    departurePlaceForm: { required, maxLength: maxLength(20) },
    arrivalPlaceForm: { required, maxLength: maxLength(20) },
    scheduleDateForm: { required },
    selectBusForm: { required },
  },

  data: () => ({
    menu2: false,

    departurePlaceForm: "",
    arrivalPlaceForm: "",
    scheduleDateForm: "",
    selectBusForm: null,
    buses: [],
    busesList: [],
    dialog: false,
    dialogDelete: false,
    headers: [
      {
        text: "Punto de Partida",
        align: "start",
        value: "departure_place",
      },
      {
        text: "Punto de Llegada",
        value: "arrival_place",
      },
      {
        text: "Horario",
        value: "schedule",
      },
      { text: "Bus", value: "bus" },
      { text: "Actions", value: "actions", sortable: false },
    ],
    destinations: [],
    destinationsFinales: [],
    editedIndex: -1,
    currentDestination: {
      id: null,
      departure_place: null,
      arrival_place: null,
      schedule: null,
      bus: null,
    },
    defaultDestination: {
      id: null,
      departure_place: null,
      arrival_place: null,
      schedule: null,
      bus: null,
    },
    newDestination: {
      departure_place: null,
      arrival_place: null,
      schedule: null,
      bus_id: null,
    },
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "Nuevo Bus" : "Edit Bus";
    },
    departurePlaceFormErrors() {
      const errors = [];
      if (!this.$v.departurePlaceForm.$dirty) return errors;
      !this.$v.departurePlaceForm.maxLength &&
        errors.push("El punto de partida debe tener máximo 20 caracteres");
      !this.$v.departurePlaceForm.required &&
        errors.push("El punto de partida es obligatorio.");
      return errors;
    },
    arrivalPlaceFormErrors() {
      const errors = [];
      if (!this.$v.arrivalPlaceForm.$dirty) return errors;
      !this.$v.arrivalPlaceForm.maxLength &&
        errors.push("El punto de llegada debe tener máximo 20 caracteres");
      !this.$v.arrivalPlaceForm.required &&
        errors.push("El punto de llegada es obligatorio.");
      return errors;
    },
    scheduleDateFormErrors() {
      const errors = [];
      if (!this.$v.scheduleDateForm.$dirty) return errors;
      !this.$v.scheduleDateForm.required &&
        errors.push("El horario es obligatorio.");
      return errors;
    },
    selectBusFormErrors() {
      const errors = [];
      if (!this.$v.selectBusForm.$dirty) return errors;
      !this.$v.selectBusForm.required && errors.push("Chofer es obligatorio");
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
    getDestinations() {
      getAPI
        .get("/api/destination/")
        .then((response) => {
          console.log("load data");
          this.destinations = response.data;
          this.destinationsFinales = [...this.destinations];
          this.destinationsFinales = this.destinations.map((d) => {
            let { bus, schedule } = d;
            schedule = new Date(schedule).toLocaleString();
            return {
              ...d,
              bus: `${bus.license_plate} - ${bus.driver.first_name} ${bus.driver.last_name}`,
              schedule,
            };
          });
        })
        .catch((err) => {
          console.log(err);
        });
    },

    createDestination(destination) {
      getAPI
        .post("/api/destination/", destination)
        .then(() => {
          console.log("created destination");
          this.getDestinations();
          this.newDestination = {};
          this.resetForm();
          this.close();
        })
        .catch((err) => {
          console.log(err);
        });
    },

    updateDestination(destination) {
      const { id } = this.currentDestination;
      getAPI
        .put(`/api/destination/${id}/`, destination)
        .then(() => {
          console.log("edited destination");
          this.getDestinations();
          this.newDestination = {};
          this.resetForm();
          this.close();
        })
        .catch((err) => {
          console.log(err);
        });
    },

    deleteDestination() {
      const { id } = this.currentDestination;
      getAPI
        .delete(`/api/destination/${id}/`)
        .then(() => {
          console.log("deleted destination");
          this.getDestinations();
          this.resetForm();
          this.close();
        })
        .catch((err) => {
          console.log(err);
        });
    },

    getBuses() {
      getAPI
        .get("/api/bus/")
        .then((response) => {
          console.log("load data");
          this.buses = response.data;
          this.busesList = this.buses.map((b) => ({
            text: `${b.license_plate} - ${b.driver.first_name} ${b.driver.last_name}`,
            value: b.id,
          }));
        })
        .catch((err) => {
          console.log(err);
        });
    },

    initialize() {
      this.getDestinations();
      this.getBuses();
    },

    editItem(item) {
      this.editedIndex = this.destinationsFinales.indexOf(item);
      this.currentDestination = this.destinations.find(
        (d) => d.id === this.destinationsFinales[this.editedIndex].id
      );
      this.departurePlaceForm = this.currentDestination.departure_place;
      this.arrivalPlaceForm = this.currentDestination.arrival_place;
      this.selectBusForm = this.currentDestination.bus.id;
      this.scheduleDateForm = this.currentDestination.schedule;
      this.dialog = true;
    },

    deleteItem(item) {
      this.editedIndex = this.destinationsFinales.indexOf(item);
      this.currentDestination = this.destinations.find(
        (d) => d.id === this.destinationsFinales[this.editedIndex].id
      );
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      this.deleteDestination();
      this.closeDelete();
    },

    close() {
      this.dialog = false;
      this.resetForm();
      this.$nextTick(() => {
        this.currentDestination = { ...this.defaultDestination };
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.currentDestination = { ...this.defaultDestination };
        this.editedIndex = -1;
      });
    },

    submit() {
      this.$v.$touch();
      if (this.$v.$invalid) return;
      this.newDestination.departure_place = this.departurePlaceForm;
      this.newDestination.arrival_place = this.arrivalPlaceForm;
      this.newDestination.schedule = new Date(this.scheduleDateForm);
      this.newDestination.bus_id = this.selectBusForm;
      this.editedIndex === -1
        ? this.createDestination(this.newDestination)
        : this.updateDestination(this.newDestination);
    },

    clear() {
      this.resetForm();
    },

    resetForm() {
      this.$v.$reset();
      this.departurePlaceForm = "";
      this.arrivalPlaceForm = "";
      this.scheduleDateForm = "";
      this.selectBusForm = null;
    },
  },
};
</script>

<style>
</style>