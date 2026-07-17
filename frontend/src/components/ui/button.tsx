import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "group/btn relative inline-flex items-center justify-center gap-2 overflow-hidden whitespace-nowrap rounded-full text-sm font-medium transition-all duration-300 ease-out focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0 [&_svg]:transition-transform [&_svg]:duration-300 active:scale-[0.98] motion-reduce:transition-none motion-reduce:active:scale-100",
  {
    variants: {
      variant: {
        default:
          // Jade gradient with a soft glow that deepens on hover; the arrow icon
          // nudges forward. A faint top sheen gives the pill a glassy finish.
          "bg-gradient-to-b from-primary to-[hsl(156_58%_44%)] text-primary-foreground shadow-glow before:absolute before:inset-x-0 before:top-0 before:h-1/2 before:rounded-t-full before:bg-white/20 before:opacity-40 before:transition-opacity before:duration-300 hover:shadow-[0_0_0_1px_hsl(var(--primary)/0.3),0_18px_50px_-12px_hsl(var(--primary)/0.55)] hover:before:opacity-60 hover:[&_svg:last-child]:translate-x-0.5",
        secondary:
          "glass text-foreground hover:border-white/20 hover:bg-white/[0.08] hover:shadow-[0_0_24px_-8px_hsl(var(--primary)/0.25)]",
        outline:
          "border border-border bg-transparent text-foreground hover:border-primary/40 hover:bg-white/[0.04]",
        ghost: "hover:bg-white/[0.06] text-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-11 px-6 py-2",
        sm: "h-9 px-4",
        lg: "h-13 px-8 text-base",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: { variant: "default", size: "default" },
  },
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    );
  },
);
Button.displayName = "Button";

export { Button, buttonVariants };
