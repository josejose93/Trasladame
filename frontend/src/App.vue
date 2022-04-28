<template>
  <v-app id="inspire">
    <v-navigation-drawer v-model="drawer" app dark>
      <!--  -->
      <v-layout mt-4 column align-center>
        <v-flex>
          <p class="white--text mt-3 headline trasladame-spacing">TRASLADAME</p>
          <v-divider></v-divider>
          <v-list dense nav>
            <v-list-item
              v-for="item in items"
              :key="item.title"
              link
              :to="item.path"
            >
              <v-list-item-action>
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-item-action>

              <v-list-item-content>
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-flex>
      </v-layout>
    </v-navigation-drawer>

    <v-app-bar class="blue accent-4 white--text" app>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>

      <v-toolbar-title class="trasladame-spacing">TRASLADAME</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <!--  -->
      <router-view />
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "App",
  data: () => {
    return {
      drawer: null,
      items: [
        { title: "Home", icon: "mdi-view-dashboard", path: "/" },
        { title: "Pasajeros", icon: "mdi-forum", path: "/pasajeros" },
        { title: "Choferes", icon: "mdi-forum", path: "/choferes" },
        { title: "Buses", icon: "mdi-forum", path: "/buses" },
        { title: "Trayectos", icon: "mdi-forum", path: "/trayectos" },
        { title: "Tickets", icon: "mdi-forum", path: "/tickets" },
        { title: "Buses Full", icon: "mdi-forum", path: "/buses-llenos" },
        {
          title: "Promedio de Pasajeros",
          icon: "mdi-forum",
          path: "/trayecto-pasajero",
        },
      ],
      links: ["Home", "Contacts", "Settings"],
      mini: true,
    };
  },
};
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400&display=swap');

.v-application {
  font-family: 'Source Sans Pro', sans-serif !important;
  font-weight: 600 !important;
}

.trasladame-spacing {
  letter-spacing: 0.5px !important;
}
</style>
