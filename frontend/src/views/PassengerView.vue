<template>
  <v-container>
    <v-data-table
      :headers="headers"
      :items="passengers"
      sort-by="last_name"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Pasajeros</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
          <v-dialog v-model="dialog" max-width="500px">
            <template v-slot:activator="{ on, attrs }">
              <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on">
                Nuevo Pasajero
              </v-btn>
            </template>

            <v-card>
              <v-card-title>
                <span class="text-h5">{{ formTitle }}</span>
              </v-card-title>

              <v-container>
                <form>
                  <v-text-field
                    v-model="firstNameForm"
                    :error-messages="firstNameFormErrors"
                    :counter="20"
                    label="Nombre"
                    required
                    @input="$v.firstNameForm.$touch()"
                    @blur="$v.firstNameForm.$touch()"
                  ></v-text-field>
                  <v-text-field
                    v-model="lastNameForm"
                    :error-messages="lastNameFormErrors"
                    :counter="20"
                    label="Apellido"
                    required
                    @input="$v.lastNameForm.$touch()"
                    @blur="$v.lastNameForm.$touch()"
                  ></v-text-field>
                  <v-text-field
                    v-model="dniForm"
                    :error-messages="dniFormErrors"
                    :counter="8"
                    label="DNI"
                    required
                    @input="$v.dniForm.$touch()"
                    @blur="$v.dniForm.$touch()"
                  ></v-text-field>

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
                >Estás seguro de borrar este pasajero?</v-card-title
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
          <h1>No se registraron Pasajeros</h1>
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
    firstNameForm: { required, maxLength: maxLength(20) },
    lastNameForm: { required, maxLength: maxLength(20) },
    dniForm: {
      required,
      maxLength: maxLength(8),
      minLength: minLength(8),
      numeric,
    },
  },

  data: () => ({
    firstNameForm: "",
    lastNameForm: "",
    dniForm: "",
    dialog: false,
    dialogDelete: false,
    headers: [
      {
        text: "First Name",
        align: "start",
        value: "first_name",
      },
      { text: "Last Name", value: "last_name" },
      { text: "DNI", value: "dni" },
      { text: "Actions", value: "actions", sortable: false },
    ],
    passengers: [],
    editedIndex: -1,
    currentPassenger: {
      id: null,
      first_name: null,
      last_name: null,
      dni: null,
    },
    defaultPassenger: {
      id: null,
      first_name: null,
      last_name: null,
      dni: null,
    },
    newPassenger: { first_name: null, last_name: null, dni: null },
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "Nuevo Pasajero" : "Edit Pasajero";
    },
    firstNameFormErrors() {
      const errors = [];
      if (!this.$v.firstNameForm.$dirty) return errors;
      !this.$v.firstNameForm.maxLength &&
        errors.push("El nombre debe tener 20 caracteres como máximo.");
      !this.$v.firstNameForm.required && errors.push("El nombre es requerido.");
      return errors;
    },
    lastNameFormErrors() {
      const errors = [];
      if (!this.$v.lastNameForm.$dirty) return errors;
      !this.$v.lastNameForm.maxLength &&
        errors.push("El apellido debe tener almenos caracteres como máximo");
      !this.$v.lastNameForm.required &&
        errors.push("El apellido es requerido.");
      return errors;
    },
    dniFormErrors() {
      const errors = [];
      if (!this.$v.dniForm.$dirty) return errors;
      !this.$v.dniForm.numeric && errors.push("El dni solo contiene números");
      !this.$v.dniForm.maxLength &&
        errors.push("El dni debe tener 8 caracteres");
      !this.$v.dniForm.minLength &&
        errors.push("El dni debe tener 8 caracteres");
      !this.$v.dniForm.required && errors.push("dni is required.");
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
    getPassengers() {
      getAPI
        .get("/api/passenger/")
        .then((response) => {
          console.log("load data");
          this.passengers = response.data;
          // console.log(this.passengers, "si");
        })
        .catch((err) => {
          console.log(err);
        });
    },

    createPassenger(passenger) {
      getAPI
        .post("/api/passenger/", passenger)
        .then(() => {
          console.log("created passenger");
          this.getPassengers();
          this.newPassenger = {};
          this.resetForm();
          this.close();
        })
        .catch((err) => {
          console.log(err);
        });
    },

    updatePassenger(passenger) {
      const { id } = this.currentPassenger;
      getAPI
        .put(`/api/passenger/${id}/`, passenger)
        .then(() => {
          console.log("edited passenger");
          this.getPassengers();
          this.newPassenger = {};
          this.resetForm();
          this.close();
        })
        .catch((err) => {
          console.log(err);
        });
    },

    deletePassenger() {
      const { id } = this.currentPassenger;
      getAPI
        .delete(`/api/passenger/${id}/`)
        .then(() => {
          console.log("deleted passenger");
          this.getPassengers();
          this.resetForm();
          this.close();
        })
        .catch((err) => {
          console.log(err);
        });
    },

    initialize() {
      this.getPassengers();
    },

    editItem(item) {
      this.editedIndex = this.passengers.indexOf(item);
      this.currentPassenger = { ...item };
      this.firstNameForm = this.currentPassenger.first_name;
      this.lastNameForm = this.currentPassenger.last_name;
      this.dniForm = this.currentPassenger.dni;
      this.dialog = true;
    },

    deleteItem(item) {
      this.editedIndex = this.passengers.indexOf(item);
      this.currentPassenger = { ...item };
      this.dialogDelete = true;
    },

    deleteItemConfirm() {
      this.deletePassenger();
      this.closeDelete();
    },

    close() {
      this.dialog = false;
      this.$v.$reset();
      this.firstNameForm = "";
      this.lastNameForm = "";
      this.dniForm = "";
      this.$nextTick(() => {
        this.currentPassenger = { ...this.defaultPassenger };
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.currentPassenger = { ...this.defaultPassenger };
        this.editedIndex = -1;
      });
    },

    save() {
      if (this.editedIndex > -1) {
        Object.assign(this.passengers[this.editedIndex], this.currentPassenger);
      } else {
        this.passengers.push(this.currentPassenger);
      }
      this.close();
    },
    submit() {
      this.$v.$touch();
      if (this.$v.$invalid) return;
      this.newPassenger.first_name = this.firstNameForm;
      this.newPassenger.last_name = this.lastNameForm;
      this.newPassenger.dni = this.dniForm;
      this.editedIndex === -1
        ? this.createPassenger(this.newPassenger)
        : this.updatePassenger(this.newPassenger);
    },
    clear() {
      this.resetForm();
    },
    resetForm() {
      this.$v.$reset();
      this.firstNameForm = "";
      this.lastNameForm = "";
      this.dniForm = "";
    },
  },
};
</script>

<style>
</style>