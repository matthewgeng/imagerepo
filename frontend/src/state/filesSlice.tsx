import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import type { RootState } from "./store";

// Define a type for the slice state
interface FilesState {
  currentFileNames: [string] | [];
}

// Define the initial state using that type
const initialState: FilesState = {
  currentFileNames: [],
};

export const filesSlice = createSlice({
  name: "files",
  // `createSlice` will infer the state type from the `initialState` argument
  initialState,
  reducers: {
    // Use the PayloadAction type to declare the contents of `action.payload`
    updateFiles: (state, action: PayloadAction<[string] | []>) => {
      state.currentFileNames = action.payload;
    },
  },
});

export const { updateFiles } = filesSlice.actions;

// Other code such as selectors can use the imported `RootState` type
export const selectFiles = (state: RootState) => state.files.currentFileNames;

export default filesSlice.reducer;
