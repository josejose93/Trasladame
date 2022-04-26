<template>
  <div class="sidebar" :style="{ width: sidebarWidth }">
    <h1>
      <span v-if="collapsed">
        <div>T</div>
        <div>S</div>
      </span>
      <span v-else>TRASLADAME</span>
    </h1>

    <SidebarLink to="/" icon="fas fa-home">Home</SidebarLink>
    <SidebarLink to="/pasajeros" icon="fas fa-user">Pasajeros</SidebarLink>
    <SidebarLink to="/choferes" icon="fas fa-user-secret">Choferes</SidebarLink>
    <SidebarLink to="/trayectos" icon="fas fa-location-pin">trayectos</SidebarLink>
    <SidebarLink to="/buses" icon="fas fa-bus-simple">Buses</SidebarLink>
    <SidebarLink to="/trayectos-pasajeros" icon="fas fa-chart-bar">Trayectos-Pasajeros</SidebarLink>
    <SidebarLink to="/buses-llenos" icon="fas fa-chart-bar">Buses con excedente</SidebarLink>

    <span
      class="collapse-icon"
      :class="{ 'rotate-180': collapsed }"
      @click="toggleSidebar"
    >
      <i class="fas fa-angle-double-left" />
    </span>
  </div>
</template>

<script>
import SidebarLink from "./SidebarLink";
import { collapsed, toggleSidebar, sidebarWidth } from "./state";

export default {
  props: {},
  components: { SidebarLink },
  setup() {
    return { collapsed, toggleSidebar, sidebarWidth };
  },
};
</script>

<style>
:root {
  --sidebar-bg-color: #007bff;
  --sidebar-item-hover: #007bff;
  --sidebar-item-active: #007bff;
}
</style>

<style scoped>
.sidebar {
  color: white;
  background-color: var(--sidebar-bg-color);
  float: left;
  position: fixed;
  z-index: 1;
  top: 0;
  left: 0;
  bottom: 0;
  padding: 0.5em;
  transition: 0.3s ease;
  display: flex;
  flex-direction: column;
}
.sidebar h1 {
  height: 2.5em;
  letter-spacing: 2px;
}
.collapse-icon {
  position: absolute;
  bottom: 0;
  padding: 0.75em;
  color: rgba(255, 255, 255, 0.7);
  transition: 0.2s linear;
}
.rotate-180 {
  transform: rotate(180deg);
  transition: 0.2s linear;
}
</style>
