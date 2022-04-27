import getAPI from "./busApi";

export const getData = async (path) => {
  const { data } = await getAPI.get(path);
  console.log("data cargada");
  console.log(data);
  // const res = [];
  // for (const id of Object.keys(data)) {
  //   res.push({ id, ...data[id] });
  // }
  return data;
};
