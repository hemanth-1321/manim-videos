"use client";

import {
  Navbar,
  NavBody,
  NavItems,
  MobileNav,
  NavbarLogo,
  NavbarButton,
  MobileNavHeader,
  MobileNavToggle,
  MobileNavMenu,
} from "@/components/ui/resizable-navbar";
import ThemeToggle from "./ThemeToggle";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useAuthStore } from "@/stores/useAuth";

export function AppBar() {
  const router = useRouter();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const { token, setToken } = useAuthStore();

  const handleLogin = () => {
    router.push("/login");
  };

  const handleLogout = () => {
    setToken(null); // Automatically clears localStorage
    router.refresh(); // Optional
  };

  return (
    <div className="relative w-full">
      <Navbar>
        <NavBody>
          <NavbarLogo />
          <div className="flex items-center gap-4">
            <ThemeToggle />
            {token ? (
              <>
                <span className="text-sm text-muted-foreground">Hello!</span>
                <NavbarButton onClick={handleLogout} variant="secondary">
                  Logout
                </NavbarButton>
              </>
            ) : (
              <NavbarButton onClick={handleLogin} variant="secondary">
                Login
              </NavbarButton>
            )}
          </div>
        </NavBody>

        {/* Mobile Navigation */}
        <MobileNav>
          <MobileNavHeader>
            <NavbarLogo />
            <div className="flex items-center gap-2">
              <ThemeToggle />
              <MobileNavToggle
                isOpen={isMobileMenuOpen}
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              />
            </div>
          </MobileNavHeader>

          <MobileNavMenu
            isOpen={isMobileMenuOpen}
            onClose={() => setIsMobileMenuOpen(false)}
          >
            <div className="flex w-full flex-col gap-4">
              {token ? (
                <>
                  <span className="text-center text-muted-foreground">Hello!</span>
                  <NavbarButton
                    onClick={() => {
                      handleLogout();
                      setIsMobileMenuOpen(false);
                    }}
                    variant="primary"
                    className="w-full"
                  >
                    Logout
                  </NavbarButton>
                </>
              ) : (
                <NavbarButton
                  onClick={() => {
                    handleLogin();
                    setIsMobileMenuOpen(false);
                  }}
                  variant="primary"
                  className="w-full"
                >
                  Login
                </NavbarButton>
              )}
            </div>
          </MobileNavMenu>
        </MobileNav>
      </Navbar>
    </div>
  );
}
