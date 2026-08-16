import type { Meta, StoryObj } from "@storybook/react-vite";
import { Alert } from "./Alert";
import { Button } from "./Button";
import { EmptyState } from "./EmptyState";
import { EnvironmentBanner } from "./EnvironmentBanner";
import { LoadingState } from "./LoadingState";
import { Skeleton } from "./Skeleton";

const meta = {
  title: "Patterns/Feedback",
  component: Alert,
} satisfies Meta<typeof Alert>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Alerts: Story = {
  render: () => (
    <div className="eh-stack">
      <Alert title="Informational">The shared component library is active.</Alert>
      <Alert title="Ready" tone="success">
        All required checks completed.
      </Alert>
      <Alert title="Review needed" tone="warning">
        This capability still uses a development adapter.
      </Alert>
      <Alert title="Unable to continue" tone="danger">
        The request could not be completed.
      </Alert>
    </div>
  ),
};

export const EnvironmentNotice: Story = {
  render: () => (
    <EnvironmentBanner
      description="No production credentials or customer data are in use."
      label="Development mode"
    />
  ),
};

export const Loading: Story = {
  render: () => <LoadingState message="Loading the component catalog…" />,
};

export const Empty: Story = {
  render: () => (
    <EmptyState
      actions={<Button>Create item</Button>}
      description="Create the first item or adjust the current filters."
      icon={<span aria-hidden="true">◇</span>}
      title="Nothing here yet"
    />
  ),
};

export const Skeletons: Story = {
  render: () => (
    <div className="eh-stack" style={{ maxWidth: "28rem" }}>
      <Skeleton shape="circle" />
      <Skeleton width="60%" />
      <Skeleton />
      <Skeleton height="10rem" shape="rectangle" />
    </div>
  ),
};
