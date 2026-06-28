import { create } from 'zustand';

type ThemePreference = 'light' | 'dark';

type UiState = {
  sidebarCollapsed: boolean;
  mobileSidebarOpen: boolean;
  themePreference: ThemePreference;
  selectedDeviceId: string | null;
  setSidebarCollapsed: (collapsed: boolean) => void;
  setMobileSidebarOpen: (open: boolean) => void;
  toggleTheme: () => void;
  setSelectedDeviceId: (deviceId: string | null) => void;
};

export const useUiStore = create<UiState>((set) => ({
  mobileSidebarOpen: false,
  selectedDeviceId: null,
  sidebarCollapsed: false,
  themePreference: 'dark',
  setMobileSidebarOpen: (open) => {
    set({ mobileSidebarOpen: open });
  },
  setSelectedDeviceId: (deviceId) => {
    set({ selectedDeviceId: deviceId });
  },
  setSidebarCollapsed: (collapsed) => {
    set({ sidebarCollapsed: collapsed });
  },
  toggleTheme: () => {
    set((state) => ({ themePreference: state.themePreference === 'dark' ? 'light' : 'dark' }));
  },
}));
