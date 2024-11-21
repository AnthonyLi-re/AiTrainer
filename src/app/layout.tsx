import * as React from 'react';
import type { Viewport } from 'next';
import Link from 'next/link';

import '@/styles/global.css';

import { UserProvider } from '@/contexts/user-context';
import { LocalizationProvider } from '@/components/core/localization-provider';
import { ThemeProvider } from '@/components/core/theme-provider/theme-provider';

import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';

export const viewport = { width: 'device-width', initialScale: 1 } satisfies Viewport;

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps): React.JSX.Element {
  return (
    <html lang="en">
      <body>
        <LocalizationProvider>
          <UserProvider>
            <ThemeProvider>
              {/* Navigation Bar */}
              <AppBar position="static" sx={{ backgroundColor: '#2C7BE5' }}>
                <Toolbar>
                  <Typography
                    variant="h6"
                    sx={{ flexGrow: 1, fontWeight: 'bold', cursor: 'pointer' }}
                    component={Link}
                    href="/"
                    color="inherit"
                  >
                    My Fitness App
                  </Typography>
                  <Box sx={{ display: 'flex', gap: '20px' }}>
                    <Button component={Link} href="/" color="inherit">
                      Dashboard
                    </Button>
                    <Button component={Link} href="/ai-trainer" color="inherit">
                      AI Trainer
                    </Button>
                    <Button component={Link} href="/meal-planner" color="inherit">
                      Meal Planner
                    </Button>
                    <Button component={Link} href="/progress-tracker" color="inherit">
                      Progress Tracker
                    </Button>
                    <Button component={Link} href="/auth/sign-in" color="inherit">
                      Sign In
                    </Button>
                  </Box>
                </Toolbar>
              </AppBar>

              {/* Page Content */}
              <Box sx={{ padding: '20px' }}>{children}</Box>
            </ThemeProvider>
          </UserProvider>
        </LocalizationProvider>
      </body>
    </html>
  );
}
