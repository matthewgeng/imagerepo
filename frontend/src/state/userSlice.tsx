import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import type { RootState } from "./store";

// Define a type for the slice state
interface UserState {
  username: string;
  uploaded: boolean;
  isUploading: boolean;
}

// Define the initial state using that type
const initialState: UserState = {
  username: "",
  uploaded: false,
  isUploading: false,
};

export const userSlice = createSlice({
  name: "user",
  // `createSlice` will infer the state type from the `initialState` argument
  initialState,
  reducers: {
    // Use the PayloadAction type to declare the contents of `action.payload`
    updateUsername: (state, action: PayloadAction<string>) => {
      state.username = action.payload;
    },
    updateUploaded: (state, action: PayloadAction<boolean>) => {
      state.uploaded = action.payload;
    },
    updateIsUploading: (state, action: PayloadAction<boolean>) => {
      state.isUploading = action.payload;
    },
  },
});

export const {
  updateUsername,
  updateUploaded,
  updateIsUploading,
} = userSlice.actions;

// Other code such as selectors can use the imported `RootState` type
export const selectUsername = (state: RootState) => state.user.username;
export const selectUploaded = (state: RootState) => state.user.uploaded;
export const selectIsUploaded = (state: RootState) => state.user.isUploading;

export default userSlice.reducer;
