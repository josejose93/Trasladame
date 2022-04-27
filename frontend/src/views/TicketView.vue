<template>
  <v-container>
    <v-data-table
      :headers="headers"
      :items="ticketsFinales"
      sort-by="passenger_id"
      class="elevation-1"
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Tickets</v-toolbar-title>
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
          <v-dialog v-model="dialog" max-width="500px">
            <template v-slot:activator="{ on, attrs }">
              <v-btn color="primary" dark class="mb-2" v-bind="attrs" v-on="on">
                Nuevo Ticket
              </v-btn>
            </template>

            <v-card>
              <v-card-title>
                <span class="text-h5">{{ formTitle }}</span>
              </v-card-title>

              <v-container>
                <form>
                  <v-select
                    v-model="selectPassengerForm"
                    :items="passengersList"
                    :error-messages="selectPassengerFormErrors"
                    label="Selecciona al pasajero"
                    required
                    @change="$v.selectPassengerForm.$touch()"
                    @blur="$v.selectPassengerForm.$touch()"
                  ></v-select>
                  <v-select
                    v-model="selectDestinationForm"
                    :items="destinationsList"
                    :error-messages="selectDestinationFormErrors"
                    label="Selecciona el trayecto"
                    required
                    @change="$v.selectDestinationForm.$touch()"
                    @blur="$v.selectDestinationForm.$touch()"
                  ></v-select>
                  <v-select
                    v-model="selectSeatForm"
                    :items="seatsList"
                    :error-messages="selectSeatFormErrors"
                    label="Selecciona el asiento"
                    required
                    @change="$v.selectSeatForm.$touch()"
                    @blur="$v.selectSeatForm.$touch()"
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
                >Estás seguro de borrar este Ticket?</v-card-title
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
          <h1>No se registraron Tickets</h1>
        </v-container>
      </template>
    </v-data-table>
  </v-container>
</template>

<script>
import getAPI from "../api/busApi";
import { validationMixin } from "vuelidate";
import { required } from "vuelidate/lib/validators";

export default {
  mixins: [validationMixin],

  validations: {
    selectPassengerForm: { required },
    selectDestinationForm: { required },
    selectSeatForm: { required },
  },

  data: () => ({
    selectPassengerForm: null,
    selectDestinationForm: null,
    selectSeatForm: null,
    passengers: [],
    destinations: [],
    seats: [],
    passengersList: [],
    destinationsList: [],
    seatsList: [
      { text: "Asiento Número 1", value: 1 },
      { text: "Asiento Número 2", value: 2 },
      { text: "Asiento Número 3", value: 3 },
      { text: "Asiento Número 4", value: 4 },
      { text: "Asiento Número 5", value: 5 },
      { text: "Asiento Número 6", value: 6 },
      { text: "Asiento Número 7", value: 7 },
      { text: "Asiento Número 8", value: 8 },
      { text: "Asiento Número 9", value: 9 },
      { text: "Asiento Número 10", value: 10 },
    ],
    seatsListDefault: [
      { text: "Asiento Número 1", value: 1 },
      { text: "Asiento Número 2", value: 2 },
      { text: "Asiento Número 3", value: 3 },
      { text: "Asiento Número 4", value: 4 },
      { text: "Asiento Número 5", value: 5 },
      { text: "Asiento Número 6", value: 6 },
      { text: "Asiento Número 7", value: 7 },
      { text: "Asiento Número 8", value: 8 },
      { text: "Asiento Número 9", value: 9 },
      { text: "Asiento Número 10", value: 10 },
    ],
    dialog: false,
    dialogDelete: false,
    headers: [
      {
        text: "Pasajero",
        align: "start",
        value: "passenger",
      },
      { text: "Trayecto", value: "destination" },
      { text: "Asiento", value: "seat" },
      { text: "Actions", value: "actions", sortable: false },
    ],
    tickets: [],
    ticketsFinales: [],
    editedIndex: -1,
    currentTicket: {
      id: null,
      passenger: null,
      destination: null,
      seat: null,
    },
    defaultTicket: {
      id: null,
      passenger: null,
      destination: null,
      seat: null,
    },
    newTicket: { passenger_id: null, destination_id: null, seat_id: null },
  }),

  computed: {
    formTitle() {
      return this.editedIndex === -1 ? "Nuevo Ticket" : "Edit Ticket";
    },

    selectPassengerFormErrors() {
      const errors = [];
      if (!this.$v.selectPassengerForm.$dirty) return errors;
      !this.$v.selectPassengerForm.required &&
        errors.push("Pasajero es obligatorio");
      return errors;
    },
    selectDestinationFormErrors() {
      const errors = [];
      if (!this.$v.selectDestinationForm.$dirty) return errors;
      !this.$v.selectDestinationForm.required &&
        errors.push("Trayecto es obligatorio");
      return errors;
    },
    selectSeatFormErrors() {
      const errors = [];
      if (!this.$v.selectSeatForm.$dirty) return errors;
      !this.$v.selectSeatForm.required && errors.push("Sitio es obligatorio");
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
    selectDestinationForm(val) {
      const seats = this.getSeats(val);
      this.seatsList =
        seats.length === 0 ? [...this.seatsListDefault] : [...seats];
    },
  },

  created() {
    this.initialize();
  },

  methods: {
    getTickets() {
      getAPI
        .get("/api/ticket/")
        .then((response) => {
          console.log("load data");
          this.tickets = response.data;
          this.ticketsFinales = this.tickets.map((d) => {
            const { passenger, destination, seat } = d;
            return {
              ...d,
              passenger: `${passenger.first_name} ${passenger.last_name}`,
              destination: `${destination.departure_place} - ${destination.arrival_place}`,
              seat: `${seat.number}`,
            };
          });
        })
        .catch((err) => {
          console.log(err);
        });
    },

    createTicket(ticket) {
      getAPI
        .post("/api/ticket/", ticket)
        .then(() => {
          console.log("created ticket");
          this.getTickets();
          this.newTicket = {};
          this.resetForm();
          this.close();
        })
        .catch((err) => {
          console.log(err);
        });
    },

    updateTicket(ticket) {
      const { id } = this.currentTicket;
      getAPI
        .put(`/api/ticket/${id}/`, ticket)
        .then(() => {
          console.log("edited ticket");
          this.getTickets();
          this.newTicket = {};
          this.resetForm();
          this.close();
        })
        .catch((err) => {
          console.log(err);
        });
    },

    deleteBuses() {
      const { id } = this.currentTicket;
      getAPI
        .delete(`/api/ticket/${id}/`)
        .then(() => {
          console.log("deleted ticket");
          this.getTickets();
          this.resetForm();
          this.close();
        })
        .catch((err) => {
          console.log(err);
        });
    },

    getPassengers() {
      getAPI
        .get("/api/passenger/")
        .then((response) => {
          console.log("load data");
          this.passengers = response.data;
          this.passengersList = this.passengers.map((p) => ({
            text: `${p.first_name} ${p.last_name}`,
            value: p.id,
          }));
        })
        .catch((err) => {
          console.log(err);
        });
    },

    getDestinations() {
      getAPI
        .get("/api/destination/")
        .then((response) => {
          console.log("load data");
          this.destinations = response.data;
          this.destinationsList = this.destinations.map((d) => ({
            text: `${d.departure_place} - ${d.arrival_place}`,
            value: d.id,
          }));
        })
        .catch((err) => {
          console.log(err);
        });
    },

    getSeats(destination) {
      const seatsNumbers = this.tickets
        .filter((t) => t.destination.id === destination)
        .map((t) => t.seat.number);
      if (seatsNumbers.length === 0) return [];

      const res = [];
      for (let i = 1; i < 11; i++) {
        const findSeat = seatsNumbers.find((n) => n === i);
        if (!findSeat) res.push({ text: `Asiento Número ${i}`, value: i });
      }

      return res;
    },

    initialize() {
      this.getTickets();
      this.getPassengers();
      this.getDestinations();
    },

    editItem(item) {
      this.editedIndex = this.ticketsFinales.indexOf(item);
      this.currentTicket = this.tickets.find(
        (t) => t.id === this.ticketsFinales[this.editedIndex].id
      );
      this.selectPassengerForm = this.currentTicket.passenger.id;
      this.selectDestinationForm = this.currentTicket.destination.id;
      this.selectSeatForm = this.currentTicket.seat.id;
      this.dialog = true;
    },

    deleteItem(item) {
      this.editedIndex = this.ticketsFinales.indexOf(item);
      this.currentTicket = this.tickets.find(
        (b) => b.id === this.ticketsFinales[this.editedIndex].id
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
        this.currentTicket = { ...this.defaultTicket };
        this.editedIndex = -1;
      });
    },

    closeDelete() {
      this.dialogDelete = false;
      this.$nextTick(() => {
        this.currentTicket = { ...this.defaultTicket };
        this.editedIndex = -1;
      });
    },

    submit() {
      this.$v.$touch();
      if (this.$v.$invalid) return;
      this.newTicket.passenger_id = this.selectPassengerForm;
      this.newTicket.destination_id = this.selectDestinationForm;
      this.newTicket.seat_id = this.selectSeatForm;
      this.editedIndex === -1
        ? this.createTicket(this.newTicket)
        : this.updateTicket(this.newTicket);
    },

    clear() {
      this.resetForm();
    },

    resetForm() {
      this.$v.$reset();
      this.selectPassengerForm = null;
      this.selectDestinationForm = null;
      this.selectSeatForm = null;
    },
  },
};
</script>

<style>
</style>