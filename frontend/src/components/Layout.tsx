import type { ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  LayoutDashboard,
  Calendar,
  Music,
  Speaker,
  Truck
} from 'lucide-react';
import { clsx } from 'clsx';

interface LayoutProps {
  children: ReactNode;
}

const navItems = [
  { path: '/', label: 'Dashboard', shortLabel: 'Home', icon: LayoutDashboard },
  { path: '/schedule', label: 'Schedule', shortLabel: 'Schedule', icon: Calendar },
  { path: '/programs', label: 'Programs', shortLabel: 'Programs', icon: Music },
  { path: '/speakers', label: 'Speakers', shortLabel: 'Speakers', icon: Speaker },
];

export function Layout({ children }: LayoutProps) {
  const location = useLocation();

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 h-14 sm:h-16 bg-gray-900 border-b border-gray-800 z-50">
        <div className="h-full px-3 sm:px-4 flex items-center justify-between">
          <div className="flex items-center gap-2 sm:gap-3">
            <Truck className="w-6 h-6 sm:w-8 sm:h-8 text-orange-500 flex-shrink-0" />
            <div className="min-w-0">
              <h1 className="text-sm sm:text-lg font-bold leading-tight truncate">World Food Trucks</h1>
              <p className="text-[10px] sm:text-xs text-gray-400 hidden sm:block">Custom Music Software V.1</p>
            </div>
          </div>
          <div className="hidden sm:flex items-center gap-2">
            <span className="text-sm text-gray-400">Control Panel</span>
          </div>
        </div>
      </header>

      {/* Desktop Sidebar - Hidden on mobile */}
      <aside className="hidden md:block fixed top-14 sm:top-16 left-0 bottom-0 w-56 bg-gray-900 border-r border-gray-800 z-40">
        <nav className="p-4 space-y-2">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            const Icon = item.icon;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={clsx(
                  'flex items-center gap-3 px-3 py-2 rounded-lg transition-colors',
                  isActive
                    ? 'bg-orange-500/20 text-orange-500'
                    : 'text-gray-400 hover:bg-gray-800 hover:text-white'
                )}
              >
                <Icon className="w-5 h-5" />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>
      </aside>

      {/* Mobile Bottom Navigation */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 h-16 bg-gray-900 border-t border-gray-800 z-50 safe-area-inset-bottom">
        <div className="h-full flex items-center justify-around px-2">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            const Icon = item.icon;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={clsx(
                  'flex flex-col items-center justify-center gap-1 px-3 py-2 rounded-lg transition-colors min-w-[60px]',
                  isActive
                    ? 'text-orange-500'
                    : 'text-gray-400 active:text-white'
                )}
              >
                <Icon className={clsx('w-5 h-5', isActive && 'drop-shadow-[0_0_8px_rgba(249,115,22,0.5)]')} />
                <span className="text-[10px] font-medium">{item.shortLabel}</span>
              </Link>
            );
          })}
        </div>
      </nav>

      {/* Main Content */}
      <main className="pt-14 sm:pt-16 md:pl-56 pb-20 md:pb-0">
        <div className="p-3 sm:p-4 md:p-6">{children}</div>
      </main>
    </div>
  );
}
