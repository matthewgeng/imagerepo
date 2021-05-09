import axios from "axios";

export const uploadFiles = (files: File[], username: string) => {
  const formData = new FormData();
  for (let i = 0; i < files.length; i++) {
    formData.append("files", files[i]);
  }
  formData.set("username", username);
  return axios({
    method: "POST",
    url: `/api/upload`,
    data: formData,
    headers: {
      "Content-Type": "multipart/form-data",
    },
  })
    .then((res) => res)
    .catch((err) => {
      console.error(err);
      throw err;
    });
};

export const getFiles = (username: string) => {
  return axios({
    method: "GET",
    url: `/api/${username}/files`,
  })
    .then((res) => res)
    .catch((err) => {
      console.error(err);
      throw err;
    });
};

export const downloadFiles = (username: string) => {
  return axios({
    method: "GET",
    responseType: "arraybuffer",
    url: `/api/${username}/download`,
  })
    .then((res) => {
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "images.zip");
      document.body.appendChild(link);
      link.click();
      link.remove();
    })
    .catch((err) => {
      console.error(err);
      throw err;
    });
};
