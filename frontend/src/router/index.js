import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/HomeView.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/pasajeros",
    name: "pasajeros",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/PassengerView.vue"),
  },
  {
    path: "/choferes",
    name: "choferes",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/DriverView.vue"),
  },
  {
    path: "/trayectos",
    name: "trayectos",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/DestinationView.vue"),
  },
  {
    path: "/buses",
    name: "buses",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/BusView.vue"),
  },
  {
    path: "/tickets",
    name: "tickets",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/TicketView.vue"),
  },
  {
    path: "/trayecto-pasajero",
    name: "trayectoPasajero",
    component: () =>
      import(
        /* webpackChunkName: "about" */ "../views/DestinationPassengerView.vue"
      ),
  },
  {
    path: "/buses-llenos",
    name: "busesLlenos",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/BusOverView.vue"),
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
