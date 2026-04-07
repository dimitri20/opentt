// For MVP: hardcode institution ID to 1
// In production, this would come from auth/context
export function useInstitution() {
  return {
    institutionId: 1,
  };
}
